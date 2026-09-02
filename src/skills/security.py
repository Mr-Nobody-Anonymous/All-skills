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
from typing import List

from .registry import Registry, SkillEntry

# Each pattern is (regex, human label, severity). High-severity findings are
# reported as validation errors; everything else is a warning. These run only
# against file *text* — no script is ever executed.
PATTERNS = [
    (re.compile(r"curl\s+.*\|\s*(sh|bash|zsh)\b", re.IGNORECASE), "pipe-to-shell pattern", "high"),
    (re.compile(r"wget\s+.*-O\s*-\s*\|\s*(sh|bash)\b", re.IGNORECASE), "wget pipe-to-shell pattern", "high"),
    (re.compile(r"\brm\s+-rf\s+/(\s|$)", re.IGNORECASE), "destructive rm -rf /", "high"),
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


@dataclass(frozen=True)
class Finding:
    skill_id: str
    path: str  # path relative to the skill folder, forward slashes
    label: str
    severity: str  # "low" | "warn" | "high"


def scan_skill(entry: SkillEntry, skill_dir: Path) -> List[Finding]:
    """Statically scan every readable file in one skill folder."""
    findings: List[Finding] = []
    if not skill_dir.exists():
        return findings
    for f in skill_dir.rglob("*"):
        if not f.is_file() or f.name.startswith("."):
            continue
        try:
            if f.stat().st_size > MAX_SCAN_FILE_SIZE:
                continue
        except OSError:
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(f.relative_to(skill_dir)).replace("\\", "/")
        for pattern, label, severity in PATTERNS:
            try:
                if pattern.search(content):
                    findings.append(Finding(entry.id, rel, label, severity))
            except Exception:
                continue
    return findings


def scan_all(registry: Registry, skills_root: Path) -> List[Finding]:
    """Static-scan every registered skill folder."""
    findings: List[Finding] = []
    for entry in registry.entries:
        skill_dir = skills_root / Path(*entry.path.split("/"))
        findings.extend(scan_skill(entry, skill_dir))
    return findings


def high_severity(findings: List[Finding]) -> List[Finding]:
    return [f for f in findings if f.severity == "high"]