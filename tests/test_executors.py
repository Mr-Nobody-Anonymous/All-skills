"""Bounded execution (SubprocessExecutor) and executor authorisation in the runtime.

Findings #1/#2 of the external review: real execution must be bounded
(isolation of the working directory and environment, resource limits,
measured usage) and an executor must not act outside what it was authorised
to do.
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
import textwrap
import time
import unittest
from pathlib import Path
from unittest import mock

_ROOT = Path(__file__).resolve().parents[1]
for _path in (_ROOT, _ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from skills.executors import ExecutorError, ProcessLimits, SubprocessExecutor  # noqa: E402
from skills.registry import SkillEntry  # noqa: E402
from skills.runtime import SkillInvocation, tool_call_violations  # noqa: E402
from tests.test_acceptance import Workspace  # noqa: E402


def invocation(inputs: dict | None = None) -> SkillInvocation:
    entry = SkillEntry(id="utilities.demo", name="demo", category="utilities", description="demo", path="utilities/demo")
    return SkillInvocation(skill=entry, inputs=inputs or {}, instructions="", authorized_capabilities=["filesystem.read"],
                           session_id=None, audit_id="audit-1")


def same_dir(a: str, b: str) -> bool:
    return os.path.normcase(os.path.realpath(a)) == os.path.normcase(os.path.realpath(b))


class ScriptCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def script(self, body: str) -> list[str]:
        path = self.tmp / f"skill_{len(list(self.tmp.iterdir()))}.py"
        path.write_text("import json, os, sys, time\n" + textwrap.dedent(body), encoding="utf-8")
        return [sys.executable, str(path)]


class TestSubprocessExecutor(ScriptCase):
    def test_runs_in_a_scratch_directory_with_a_scrubbed_environment(self):
        argv = self.script("""
            payload = json.load(sys.stdin)
            print(json.dumps({"outputs": {
                "cwd": os.getcwd(), "home": os.environ.get("HOME"),
                "secret": os.environ.get("ALLSKILLS_TEST_SECRET"),
                "inputs": payload["inputs"], "caps": payload["authorized_capabilities"],
            }, "usage": {"tokens": 7}}))
        """)
        with mock.patch.dict(os.environ, {"ALLSKILLS_TEST_SECRET": "hunter2"}):
            result = SubprocessExecutor(argv)(invocation({"q": "hello"}))
        out = result["outputs"]
        self.assertIsNone(out["secret"], "the parent's environment must not leak into the skill")
        self.assertTrue(same_dir(out["cwd"], out["home"]), "HOME is the per-run scratch directory")
        self.assertFalse(same_dir(out["cwd"], os.getcwd()))
        self.assertFalse(Path(out["cwd"]).exists(), "the scratch directory is removed after the run")
        self.assertEqual((out["inputs"], out["caps"]), ({"q": "hello"}, ["filesystem.read"]))
        usage = result["usage"]
        self.assertEqual(usage["exit_code"], 0)
        self.assertGreater(usage["wall_ms"], 0)
        self.assertEqual(usage["reported"], {"tokens": 7}, "self-reported usage is kept apart from measurements")
        if os.name == "posix":
            self.assertIn("cpu_s", usage)

    def test_timeout_kills_the_process_group(self):
        pid_file = self.tmp / "pid"
        argv = self.script(f"""
            import subprocess
            child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(60)"])
            open({str(pid_file)!r}, "w").write(str(child.pid))
            time.sleep(60)
        """)
        started = time.monotonic()
        with self.assertRaisesRegex(ExecutorError, "timed out"):
            SubprocessExecutor(argv, ProcessLimits(timeout_s=2))(invocation())
        self.assertLess(time.monotonic() - started, 30)
        if os.name == "posix" and pid_file.exists():
            grandchild = int(pid_file.read_text())
            deadline = time.monotonic() + 5
            while time.monotonic() < deadline:
                try:
                    os.kill(grandchild, 0)
                except ProcessLookupError:
                    break
                time.sleep(0.1)
            else:
                self.fail("a process started by the skill survived the timeout")

    def test_protocol_violations_fail(self):
        cases = {
            "exited with status 3: boom": "sys.stderr.write('boom'); sys.exit(3)",
            "did not print a JSON object": "print('not json')",
            "expected an object": "print(json.dumps([1, 2]))",
            "more than 100 bytes": "print(json.dumps({'outputs': {'x': 'y' * 500}}))",
        }
        for message, body in cases.items():
            with self.subTest(message), self.assertRaisesRegex(ExecutorError, message):
                SubprocessExecutor(self.script(body), ProcessLimits(max_output_bytes=100))(invocation())
        with self.assertRaisesRegex(ExecutorError, "could not start"):
            SubprocessExecutor([str(self.tmp / "no-such-command")])(invocation())

    @unittest.skipUnless(os.name == "posix", "setrlimit is POSIX-only")
    def test_file_size_limit_is_enforced(self):
        argv = self.script("""
            with open("big.bin", "wb") as fh:
                fh.write(b"x" * (4 * 1024 * 1024))
            print(json.dumps({"outputs": {}}))
        """)
        with self.assertRaisesRegex(ExecutorError, "File too large|SIGXFSZ"):
            SubprocessExecutor(argv, ProcessLimits(max_file_bytes=64 * 1024))(invocation())

    @unittest.skipIf(os.name == "posix", "only platforms without setrlimit refuse limits")
    def test_limits_that_cannot_be_enforced_are_refused(self):
        with self.assertRaisesRegex(ExecutorError, "cannot be enforced"):
            SubprocessExecutor([sys.executable, "-c", "pass"], ProcessLimits(cpu_seconds=5))


class TestExecutorAuthorisation(ScriptCase):
    """The runtime fails any run whose reported tool calls exceed its authorisation."""

    def setUp(self):
        super().setUp()
        self.ws = Workspace()
        self.skill_id = self.ws.add_skill("worker", tools=("file_read",), outputs=("answer",))

    def tearDown(self):
        self.ws.cleanup()
        super().tearDown()

    def run_with(self, tool_calls: list) -> object:
        argv = self.script(f"print(json.dumps({{'outputs': {{'answer': 42}}, 'tool_calls': {tool_calls!r}}}))")
        runtime = self.ws.runtime()
        runtime.register_executor(self.skill_id, SubprocessExecutor(argv))
        return runtime.execute(self.skill_id)

    def test_authorised_run_completes_with_measured_usage(self):
        result = self.run_with([{"tool": "file_read"}])
        self.assertEqual(result.status, "completed", result.error)
        self.assertEqual(result.outputs, {"answer": 42})
        self.assertIn("wall_ms", result.cost["executor_usage"])
        self.assertEqual(result.verification["capability_violations"], [])

    def test_unauthorised_or_unnamed_tool_calls_fail_the_run(self):
        for calls, needle in (([{"tool": "bash"}], "bash"), ([{"tool": "teleport"}], "teleport"),
                              ([{"args": "x"}], "does not name its tool")):
            with self.subTest(calls=calls):
                result = self.run_with(calls)
                self.assertEqual(result.status, "failed")
                self.assertIn("outside its authorisation", result.error)
                self.assertIn(needle, "; ".join(result.verification["capability_violations"]))
                self.assertFalse(result.verification["verified"])
        self.assertEqual(self.ws.audit_statuses()[-1], "failed")

    def test_unclassified_tools_are_only_authorised_by_name(self):
        caps = ["filesystem.read", "tool.unclassified"]
        self.assertEqual(tool_call_violations([{"tool": "foo"}], ["foo"], caps), [])
        self.assertEqual(len(tool_call_violations([{"tool": "bar"}], ["foo"], caps)), 1,
                         "approving one unknown tool must not authorise another")


if __name__ == "__main__":
    unittest.main()
