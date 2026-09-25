"""Bounded executors for :class:`skills.runtime.ExecutionRuntime`.

:class:`SubprocessExecutor` runs a skill's command in a separate process and
gives every run:

* a fresh temporary working directory, also used as ``HOME``/``TMPDIR``, that is
  removed afterwards;
* an environment reduced to an allow-list, so credentials and tokens in the
  parent's environment are not inherited;
* a wall-clock timeout that kills the whole process group (POSIX) or the
  process (Windows);
* a cap on the output it may return;
* on POSIX, optional CPU-time, address-space and file-size limits, applied with
  ``setrlimit`` before the command starts — if a requested limit cannot be
  applied the command does not run, and requesting them on a platform without
  ``setrlimit`` is refused up front;
* usage measured on the runtime side (wall time, exit status and, on POSIX,
  child CPU time), independent of anything the command reports about itself.

Protocol: the command receives one JSON object on stdin —
``{"skill", "inputs", "authorized_capabilities", "audit_id"}`` — and must print
one JSON object on stdout: ``{"outputs": {...}, "artifacts": [...],
"tool_calls": [...], "usage": {...}}`` (everything except ``outputs`` is
optional; self-reported usage is kept under ``usage.reported``).

This bounds *resources*; it is **not** a security sandbox. The command can still
read any file the user can read and open network connections. Run untrusted
code inside OS-level isolation (a container or VM) — see docs/LIMITATIONS.md.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Optional, Sequence

if TYPE_CHECKING:  # pragma: no cover
    from .runtime import SkillInvocation

# Variables a process needs to start and behave predictably. Everything else in
# the parent's environment (API keys, tokens, cloud credentials) is dropped.
DEFAULT_ENV_ALLOWLIST = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TZ", "SYSTEMROOT", "WINDIR", "COMSPEC", "PATHEXT")

_STDERR_TAIL = 2000

# Runs in the child before the real command: apply the limits, then exec the
# command in the same process (no preexec_fn, so it is safe in threaded
# parents). Exit status 126 means the limits could not be applied.
_BOOTSTRAP = (
    "import json, os, resource, sys\n"
    "try:\n"
    "    for name, value in json.loads(sys.argv[1]).items():\n"
    "        resource.setrlimit(getattr(resource, name), (value, value))\n"
    "except (AttributeError, ValueError, OSError) as exc:\n"
    "    sys.stderr.write('could not apply resource limits: %s\\n' % exc)\n"
    "    sys.exit(126)\n"
    "os.execvp(sys.argv[2], sys.argv[2:])\n"
)


class ExecutorError(RuntimeError):
    """The command could not run, exceeded a limit, or broke the protocol."""


@dataclass(frozen=True)
class ProcessLimits:
    """Resource bounds for one run. ``None`` leaves a POSIX limit unset."""

    timeout_s: float = 60.0
    max_output_bytes: int = 1_000_000
    cpu_seconds: Optional[int] = None  # RLIMIT_CPU (POSIX only)
    memory_bytes: Optional[int] = None  # RLIMIT_AS (POSIX only)
    max_file_bytes: Optional[int] = None  # RLIMIT_FSIZE (POSIX only)

    def rlimits(self) -> Dict[str, int]:
        pairs = {"RLIMIT_CPU": self.cpu_seconds, "RLIMIT_AS": self.memory_bytes, "RLIMIT_FSIZE": self.max_file_bytes}
        return {name: int(value) for name, value in pairs.items() if value is not None}


def _children_cpu_seconds() -> Optional[float]:
    try:
        import resource
    except ImportError:  # Windows
        return None
    usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    return float(usage.ru_utime + usage.ru_stime)


def _kill(proc: "subprocess.Popen[bytes]") -> None:
    """Kill the process and, on POSIX, everything it started (its session)."""
    if os.name == "posix":
        try:
            os.killpg(proc.pid, getattr(signal, "SIGKILL", signal.SIGTERM))
            return
        except (ProcessLookupError, PermissionError, OSError):
            pass
    proc.kill()


def _describe_exit(returncode: int) -> str:
    if returncode < 0:
        try:
            return f"was killed by {signal.Signals(-returncode).name}"
        except ValueError:
            return f"was killed by signal {-returncode}"
    return f"exited with status {returncode}"


class SubprocessExecutor:
    """Run ``argv`` as the executor of a skill, bounded by :class:`ProcessLimits`."""

    def __init__(
        self,
        argv: Sequence[str],
        limits: Optional[ProcessLimits] = None,
        env_allowlist: Sequence[str] = DEFAULT_ENV_ALLOWLIST,
        extra_env: Optional[Mapping[str, str]] = None,
    ) -> None:
        if not argv:
            raise ValueError("argv must name the command to run")
        self.argv: List[str] = [str(part) for part in argv]
        self.limits = limits or ProcessLimits()
        if self.limits.timeout_s <= 0 or self.limits.max_output_bytes <= 0:
            raise ValueError("timeout_s and max_output_bytes must be positive")
        if self.limits.rlimits() and os.name != "posix":
            raise ExecutorError("CPU, memory and file-size limits need POSIX setrlimit and cannot be "
                                "enforced on this platform; refusing to run without them")
        self.env_allowlist = tuple(env_allowlist)
        self.extra_env = dict(extra_env or {})

    def command(self) -> List[str]:
        """The command line actually started (wrapped when limits apply)."""
        rlimits = self.limits.rlimits()
        if not rlimits:
            return list(self.argv)
        return [sys.executable, "-c", _BOOTSTRAP, json.dumps(rlimits), *self.argv]

    def environment(self, workdir: str) -> Dict[str, str]:
        env = {key: os.environ[key] for key in self.env_allowlist if key in os.environ}
        env.update({"HOME": workdir, "USERPROFILE": workdir, "TMPDIR": workdir, "TEMP": workdir, "TMP": workdir})
        env.update(self.extra_env)
        return env

    def __call__(self, invocation: "SkillInvocation") -> Dict[str, Any]:
        payload = json.dumps(
            {
                "skill": invocation.skill.id,
                "inputs": invocation.inputs,
                "authorized_capabilities": list(invocation.authorized_capabilities),
                "audit_id": invocation.audit_id,
            },
            default=str,
        ).encode("utf-8")
        name = os.path.basename(self.argv[0])
        with tempfile.TemporaryDirectory(prefix="allskills-run-", ignore_cleanup_errors=True) as workdir, \
                tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
            popen_kwargs: Dict[str, Any] = {
                "stdin": subprocess.PIPE, "stdout": out, "stderr": err,
                "cwd": workdir, "env": self.environment(workdir),
            }
            if os.name == "posix":
                popen_kwargs["start_new_session"] = True
            else:
                popen_kwargs["creationflags"] = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
            cpu_before = _children_cpu_seconds()
            started = time.perf_counter()
            try:
                proc = subprocess.Popen(self.command(), **popen_kwargs)
            except OSError as exc:
                raise ExecutorError(f"could not start {name}: {exc}") from exc
            try:
                proc.communicate(payload, timeout=self.limits.timeout_s)
            except subprocess.TimeoutExpired:
                _kill(proc)
                proc.wait()
                raise ExecutorError(f"{name} timed out after {self.limits.timeout_s:g}s and was killed") from None
            wall_ms = (time.perf_counter() - started) * 1000

            usage: Dict[str, Any] = {"wall_ms": round(wall_ms, 3), "exit_code": proc.returncode}
            cpu_after = _children_cpu_seconds()
            if cpu_before is not None and cpu_after is not None:
                usage["cpu_s"] = round(max(cpu_after - cpu_before, 0.0), 6)

            err.seek(0)
            stderr_tail = err.read().decode("utf-8", "replace").strip()[-_STDERR_TAIL:]
            if proc.returncode != 0:
                raise ExecutorError(f"{name} {_describe_exit(proc.returncode)}" + (f": {stderr_tail}" if stderr_tail else ""))
            out.seek(0)
            stdout = out.read(self.limits.max_output_bytes + 1)
            if len(stdout) > self.limits.max_output_bytes:
                raise ExecutorError(f"{name} printed more than {self.limits.max_output_bytes} bytes")
            try:
                result = json.loads(stdout.decode("utf-8"))
            except (UnicodeDecodeError, ValueError) as exc:
                raise ExecutorError(f"{name} did not print a JSON object on stdout ({exc})") from None
            if not isinstance(result, dict):
                raise ExecutorError(f"{name} printed JSON {type(result).__name__}, expected an object")

        reported = result.get("usage")
        if isinstance(reported, Mapping):
            usage["reported"] = dict(reported)
        result["usage"] = usage
        return result
