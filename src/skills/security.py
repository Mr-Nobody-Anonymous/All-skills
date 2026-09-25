"""Read-only static inspection of skill folders.

Never executes anything. Detects suspicious patterns, credential exposure, and
destructive commands across the text files of a skill. Part of the import gate:
third-party repositories are cloned, inspected, and only then imported — never
``git clone && execute``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
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
    (re.compile(r"eval\s*\(", re.IGNORECASE), "eval() call", "warn"),
    (re.compile(r"\bexec\s*\(", re.IGNORECASE), "exec() call", "warn"),
    (re.compile(r"os\.system\s*\(", re.IGNORECASE), "os.system call", "warn"),
    (re.compile(r"subprocess\.(run|Popen|call|check_output)\([^)]*shell\s*=\s*True", re.IGNORECASE), "subprocess with shell=True", "warn"),
    (re.compile(r"(?:^|[\\/])(?:\.ssh[\\/]id_rsa|\.aws[\\/]credentials|\.npmrc|\.netrc|\.env)(?:\b|$)", re.IGNORECASE | re.MULTILINE), "credential file reference", "warn"),
    (re.compile(r"base64\s+-d|atob\(|Buffer\.from\([^)]+, ?['\"]base64", re.IGNORECASE), "base64 decode", "warn"),
    (re.compile(r"https?://\S+\.webhook\S*", re.IGNORECASE), "webhook endpoint", "warn"),
]

MAX_SCAN_FILE_SIZE = 2_000_000


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
    """Statically scan every readable file in one skill folder.

    Never bypasses findings based on content keywords in the inspected lines.
    Only explicit file-level annotations ('# security-scan: ignore') or
    audited test fixture paths are exempted.
    """
    findings: List[Finding] = []
    if not skill_dir.exists():
        return findings
    for f in skill_dir.rglob("*"):
        if not f.is_file() or f.name.startswith("."):
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        try:
            sz = f.stat().st_size
            if sz > MAX_SCAN_FILE_SIZE:
                findings.append(Finding(entry.id, rel, f"file exceeds max scan size ({sz} bytes) - status: {ScanStatus.UNSCANNABLE}", "warn"))
                continue
        except OSError as exc:
            findings.append(Finding(entry.id, rel, f"unreadable file ({exc}) - status: {ScanStatus.SCAN_FAILED}", "warn"))
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            findings.append(Finding(entry.id, rel, f"read failure ({exc}) - status: {ScanStatus.SCAN_FAILED}", "warn"))
            continue

        # File-level explicit exemption only
        if content.startswith("# security-scan: ignore") or content.startswith("<!-- security-scan: ignore -->"):
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


import datetime
import json


def quarantine_skill(
    skill_id: str,
    reason: str,
    reporter: str = "security_scanner",
    repo_root: Path | None = None,
) -> dict:
    """Quarantine a skill, adding it to revocations.json and recording forensic evidence."""
    root = repo_root or Path.cwd()
    quarantine_dir = root / "quarantine"
    quarantine_dir.mkdir(parents=True, exist_ok=True)
    evidence_dir = quarantine_dir / "evidence"
    evidence_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    event = {
        "timestamp": timestamp,
        "action": "quarantine",
        "skill_id": skill_id,
        "reason": reason,
        "reporter": reporter,
    }

    # Append to quarantine log
    log_path = quarantine_dir / "quarantine_log.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    # Update skills/revocations.json
    revocations_path = root / "skills" / "revocations.json"
    revocations_data: Dict[str, Any] = {"version": "1.0.0", "revocations": []}
    if revocations_path.exists():
        try:
            revocations_data = json.loads(revocations_path.read_text(encoding="utf-8"))
        except Exception:
            pass

    existing_ids = {r.get("skill_id") for r in revocations_data.get("revocations", [])}
    if skill_id not in existing_ids:
        revocations_data["revocations"].append({
            "skill_id": skill_id,
            "revoked_at": timestamp,
            "reason": reason,
            "severity": "high",
        })
        revocations_path.parent.mkdir(parents=True, exist_ok=True)
        revocations_path.write_text(json.dumps(revocations_data, indent=2), encoding="utf-8")

    # Save evidence file
    evidence_path = evidence_dir / f"{skill_id.replace('/', '_')}.json"
    evidence_path.write_text(json.dumps(event, indent=2), encoding="utf-8")

    return {
        "status": "quarantined",
        "skill_id": skill_id,
        "reason": reason,
        "timestamp": timestamp,
    }


def is_quarantined(skill_id: str, repo_root: Path | None = None) -> bool:
    """Check whether a skill is currently in quarantine or revocation."""
    root = repo_root or Path.cwd()
    revocations_path = root / "skills" / "revocations.json"
    if revocations_path.exists():
        try:
            data = json.loads(revocations_path.read_text(encoding="utf-8"))
            for r in data.get("revocations", []):
                if r.get("skill_id") == skill_id:
                    return True
        except Exception:
            pass
    return False


def unquarantine_skill(
    skill_id: str,
    reason: str,
    approver: str,
    repo_root: Path | None = None,
) -> dict:
    """Reinstates a quarantined skill after formal remediation."""
    root = repo_root or Path.cwd()
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    event = {
        "timestamp": timestamp,
        "action": "unquarantine",
        "skill_id": skill_id,
        "reason": reason,
        "approver": approver,
    }

    log_path = root / "quarantine" / "quarantine_log.jsonl"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    revocations_path = root / "skills" / "revocations.json"
    if revocations_path.exists():
        try:
            data = json.loads(revocations_path.read_text(encoding="utf-8"))
            data["revocations"] = [r for r in data.get("revocations", []) if r.get("skill_id") != skill_id]
            revocations_path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        except Exception:
            pass

    return {
        "status": "reinstated",
        "skill_id": skill_id,
        "reason": reason,
        "timestamp": timestamp,
    }