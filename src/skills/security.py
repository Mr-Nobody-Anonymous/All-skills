"""Read-only static inspection of skill folders.

Never executes anything. Detects suspicious patterns, credential exposure, and
destructive commands across the text files of a skill. Part of the import gate:
third-party repositories are cloned, inspected, and only then imported — never
``git clone && execute``.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from .registry import Registry, SkillEntry

# Each pattern is (regex, human label, severity). High-severity findings are
# reported as validation errors; everything else is a warning. These run only
# against file *text* — no script is ever executed.
PATTERNS = [
    (re.compile(r"curl\s+.*\|\s*(sh|bash|zsh)\b", re.IGNORECASE), "pipe-to-shell pattern", "high"),
    (re.compile(r"wget\s+.*-O\s*-\s*\|\s*(sh|bash)\b", re.IGNORECASE), "wget pipe-to-shell pattern", "high"),
    (re.compile(r"\brm\s+-rf\s+/(\s|$)", re.IGNORECASE), "destructive rm -rf /", "high"),
    (re.compile(r"\bdd\s+if=/dev/zero\s+of=/dev/[a-z]+", re.IGNORECASE), "destructive dd disk overwrite", "high"),
    (re.compile(r"\bmkfs\.[a-z0-9]+\s+/dev/", re.IGNORECASE), "destructive filesystem formatting", "high"),
    (re.compile(r"(?i)\bignore\s+(all\s+)?(previous|prior)\s+instructions\b"), "prompt injection: ignore previous instructions", "high"),
    (re.compile(r"(?i)\bdisregard\s+(all\s+)?(previous|above)\s+instructions\b"), "prompt injection: disregard instructions", "high"),
    (re.compile(r"(?i)<\s*system_override\s*>"), "prompt injection: system override tag", "high"),
    (re.compile(r"powershell\s+-e(ncodedcommand)?\s+\S+", re.IGNORECASE), "powershell encoded command", "high"),
    (re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"), "embedded private key", "high"),
    (re.compile(r"\b(AKIA|ASIA)[0-9A-Z]{16}\b"), "AWS access key", "high"),
    (re.compile(r"\beval\s*\(", re.IGNORECASE), "eval() call", "warn"),
    (re.compile(r"\bexec\s*\(", re.IGNORECASE), "exec() call", "warn"),
    (re.compile(r"os\.system\s*\(", re.IGNORECASE), "os.system call", "warn"),
    (re.compile(r"subprocess\.(run|Popen|call|check_output)\([^)]*shell\s*=\s*True", re.IGNORECASE), "subprocess with shell=True", "warn"),
    (re.compile(r"(?:^|[\\/])(?:\.ssh[\\/]id_rsa|\.aws[\\/]credentials|\.npmrc|\.netrc|\.env)(?:\b|$)", re.IGNORECASE | re.MULTILINE), "credential file reference", "warn"),
    (re.compile(r"base64\s+-d|atob\(|Buffer\.from\([^)]+, ?['\"]base64", re.IGNORECASE), "base64 decode", "warn"),
    (re.compile(r"https?://\S+\.webhook\S*", re.IGNORECASE), "webhook endpoint", "warn"),
]

MAX_SCAN_FILE_SIZE = 2_000_000
ALLOWLIST_RELPATH = Path("registry") / "security_allowlist.json"
INCOMPLETE = "incomplete"  # severity of findings that mean "this file was not scanned"


class ScanStatus:
    SCANNED = "SCANNED"
    SCANNED_WITH_LIMIT = "SCANNED_WITH_LIMIT"
    SCAN_FAILED = "SCAN_FAILED"
    UNSCANNABLE = "UNSCANNABLE"


import ast
import yaml


@dataclass(frozen=True)
class Finding:
    skill_id: str
    path: str  # path relative to the skill folder, forward slashes
    label: str
    severity: str  # "low" | "warn" | "high"


def scan_skill(entry: SkillEntry, skill_dir: Path) -> List[Finding]:
    """Statically scan every file in one skill folder, including dotfiles.

    Files cannot exempt themselves: content markers are ignored and exceptions
    live only in the maintainer-controlled allowlist (see :func:`apply_allowlist`).
    Files that could not be inspected produce ``incomplete`` findings, so an
    unscanned package is never reported as clean.
    """
    findings: List[Finding] = []
    if not skill_dir.exists():
        return findings
    for f in sorted(skill_dir.rglob("*")):
        rel_parts = f.relative_to(skill_dir).parts
        if ".git" in rel_parts or "__pycache__" in rel_parts or not f.is_file():
            continue
        rel = "/".join(rel_parts)
        try:
            sz = f.stat().st_size
        except OSError as exc:
            findings.append(Finding(entry.id, rel, f"unreadable file ({exc}) - status: {ScanStatus.SCAN_FAILED}", INCOMPLETE))
            continue
        if sz > MAX_SCAN_FILE_SIZE:
            findings.append(Finding(entry.id, rel, f"file exceeds max scan size ({sz} bytes) - status: {ScanStatus.UNSCANNABLE}", INCOMPLETE))
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except OSError as exc:
            findings.append(Finding(entry.id, rel, f"read failure ({exc}) - status: {ScanStatus.SCAN_FAILED}", INCOMPLETE))
            continue

        for pattern, label, severity in PATTERNS:
            try:
                for match in pattern.finditer(content):
                    findings.append(Finding(entry.id, rel, label, severity))
                    break
            except Exception:
                continue
    return findings


def check_python_ast(file_path: Path) -> tuple[bool, str]:
    """Parse Python code into AST to detect syntax errors and malformed scripts."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        ast.parse(content, filename=str(file_path))
        return True, "valid"
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} on line {e.lineno}"
    except Exception as e:
        return False, str(e)


def check_yaml_ast(file_path: Path) -> tuple[bool, str]:
    """Verify YAML file syntactic validity via safe loading."""
    try:
        content = file_path.read_text(encoding="utf-8", errors="ignore")
        yaml.safe_load(content)
        return True, "valid"
    except Exception as e:
        return False, str(e)


def scan_all(registry: Registry, skills_root: Path) -> List[Finding]:
    """Static-scan every registered skill folder."""
    findings: List[Finding] = []
    for entry in registry.entries:
        skill_dir = skills_root / Path(*entry.path.split("/"))
        findings.extend(scan_skill(entry, skill_dir))
    return findings


def high_severity(findings: List[Finding]) -> List[Finding]:
    return [f for f in findings if f.severity == "high"]


def scan_is_complete(findings: List[Finding]) -> bool:
    """False if any file could not be inspected (unscannable or unreadable)."""
    return not any(f.severity == INCOMPLETE for f in findings)


def load_allowlist(workspace_root: Path) -> List[Dict[str, Any]]:
    """Maintainer-reviewed scanner exceptions (``registry/security_allowlist.json``).

    Every entry must name the skill, file, finding label, a reason and the
    file's SHA-256 at review time; editing the file invalidates the exception.
    """
    path = Path(workspace_root) / ALLOWLIST_RELPATH
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = data.get("entries") if isinstance(data, dict) else None
    if not isinstance(entries, list):
        raise ValueError(f"{path}: 'entries' must be a list")
    required = ("skill", "path", "label", "reason", "sha256")
    for entry in entries:
        if not isinstance(entry, dict) or any(not entry.get(k) for k in required):
            raise ValueError(f"{path}: every entry needs {', '.join(required)}: {entry!r}")
    return entries


def apply_allowlist(
    findings: List[Finding],
    allowlist: List[Dict[str, Any]],
    skill_dirs: Dict[str, Path],
) -> tuple[List[Finding], List[Finding], List[Dict[str, Any]]]:
    """Split findings into (active, suppressed) and report stale allowlist entries.

    ``skill_dirs`` maps each finding's ``skill_id`` to its folder so the file
    hash can be checked against the reviewed hash.
    """
    from .lock import compute_file_sha256

    active: List[Finding] = []
    suppressed: List[Finding] = []
    used: set[int] = set()
    for finding in findings:
        match = None
        for idx, entry in enumerate(allowlist):
            if (entry["skill"], entry["path"], entry["label"]) != (finding.skill_id, finding.path, finding.label):
                continue
            skill_dir = skill_dirs.get(finding.skill_id)
            file_path = skill_dir / finding.path if skill_dir else None
            if file_path and file_path.is_file() and compute_file_sha256(file_path) == entry["sha256"]:
                match = idx
                break
        if match is None:
            active.append(finding)
        else:
            used.add(match)
            suppressed.append(finding)
    stale = [entry for idx, entry in enumerate(allowlist) if idx not in used]
    return active, suppressed, stale


INSTRUCTION_PATTERNS = [
    (re.compile(r"(?i)\bignore\s+(all\s+)?(previous|prior)\s+instructions\b"), "prompt injection: ignore previous instructions", "high"),
    (re.compile(r"(?i)\bdisregard\s+(all\s+)?(previous|above)\s+instructions\b"), "prompt injection: disregard instructions", "high"),
    (re.compile(r"(?i)<\s*system_override\s*>"), "prompt injection: system override tag", "high"),
    (re.compile(r"(?i)\breveal\s+(the\s+)?(system\s+prompt|instructions)\b"), "prompt injection: reveal system prompt", "high"),
    (re.compile(r"(?i)\b(send|exfiltrate|post)\s+.*(credentials|api[_-]?keys?|secrets?|tokens?)\b"), "prompt injection: credential exfiltration", "high"),
    (re.compile(r"(?i)\b(disable|turn\s+off|bypass)\s+.*(security|policy|guardrails?|sandbox)\b"), "prompt injection: security bypass", "high"),
    (re.compile(r"(?i)\bexecute\s+.*without\s+(any\s+)?(confirmation|approval|asking)\b"), "prompt injection: unconfirmed execution", "warn"),
    (re.compile(r"(?i)\bhide\s+this\s+(action|command|execution)\s+from\s+(the\s+)?user\b"), "prompt injection: covert execution", "high"),
]


def scan_instructions(text: str) -> List[tuple[str, str]]:
    """Scan instruction or prompt text for injection patterns and safety bypasses.

    Returns list of (label, severity) tuples.
    """
    findings: List[tuple[str, str]] = []
    for pattern, label, severity in INSTRUCTION_PATTERNS:
        if pattern.search(text):
            findings.append((label, severity))
    return findings


from .revocations import add_revocation, get_revocation, remove_revocation


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def quarantine_skill(
    skill_id: str,
    reason: str,
    reporter: str = "security_scanner",
    repo_root: Path | None = None,
) -> dict:
    """Quarantine a skill: revoke it in registry/revocations.json and record forensic evidence.

    Uses the same revocation contract as the router and the execution runtime
    (:mod:`skills.revocations`), so a quarantined skill can no longer be routed
    or executed.
    """
    root = repo_root or Path.cwd()
    quarantine_dir = root / "quarantine"
    evidence_dir = quarantine_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    timestamp = _utc_now()
    event = {
        "timestamp": timestamp,
        "action": "quarantine",
        "skill_id": skill_id,
        "reason": reason,
        "reporter": reporter,
    }
    with open(quarantine_dir / "quarantine_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    add_revocation(root, skill_id, reason, severity="high", reporter=reporter)

    evidence_path = evidence_dir / f"{skill_id.replace('/', '_')}.json"
    evidence_path.write_text(json.dumps(event, indent=2), encoding="utf-8")

    return {"status": "quarantined", "skill_id": skill_id, "reason": reason, "timestamp": timestamp}


def is_quarantined(skill_id: str, repo_root: Path | None = None) -> bool:
    """Whether a skill is revoked or quarantined.

    Raises :class:`skills.revocations.RevocationError` if the registry is
    malformed — "unknown" must never be reported as "not quarantined".
    """
    return get_revocation(skill_id, repo_root or Path.cwd()) is not None


def unquarantine_skill(
    skill_id: str,
    reason: str,
    approver: str,
    repo_root: Path | None = None,
) -> dict:
    """Reinstate a quarantined skill after formal remediation (records who approved it)."""
    root = repo_root or Path.cwd()
    timestamp = _utc_now()
    event = {
        "timestamp": timestamp,
        "action": "unquarantine",
        "skill_id": skill_id,
        "reason": reason,
        "approver": approver,
    }
    (root / "quarantine").mkdir(parents=True, exist_ok=True)
    with open(root / "quarantine" / "quarantine_log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    remove_revocation(root, skill_id)

    return {
        "status": "reinstated",
        "skill_id": skill_id,
        "reason": reason,
        "timestamp": timestamp,
    }
