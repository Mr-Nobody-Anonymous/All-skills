"""Skill validation — checks SKILL.md, paths, conflicts, and basic safety."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Set

from .registry import Registry, SkillEntry


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.ok = False

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        self.info.append(msg)


REQUIRED_FRONTMATTER = {"name", "description", "category", "version"}
REQUIRED_SECTIONS = {
    "Purpose", "When to Use", "When NOT to Use", "Capabilities", "Inputs",
    "Workflow", "Tools", "Examples", "Safety", "Source", "Notes",
}
SUSPICIOUS_PATTERNS = [
    (re.compile(r"curl\s+.*\|\s*(sh|bash)", re.IGNORECASE), "pipe-to-shell pattern"),
    (re.compile(r"eval\s*\(", re.IGNORECASE), "eval() call"),
    (re.compile(r"base64\s+-d|atob\(|Buffer\.from\([^)]+, ?['\"]base64", re.IGNORECASE), "base64 decode"),
    (re.compile(r"(?:^|[\\/])(?:\.ssh[\\/]id_rsa|\.aws[\\/]credentials|\.npmrc|\.netrc|\.env)(?:\b|$)", re.IGNORECASE | re.MULTILINE), "credential file reference"),
    (re.compile(r"\brm\s+-rf\s+/", re.IGNORECASE), "destructive rm -rf /"),
    (re.compile(r"powershell\s+-e(ncodedcommand)?\s+", re.IGNORECASE), "powershell encoded command"),
]


class Validator:
    def __init__(self, registry: Registry, skills_root: Path) -> None:
        self.registry = registry
        self.skills_root = skills_root

    def validate_all(self) -> ValidationResult:
        result = ValidationResult(ok=True)
        ids_seen: Set[str] = set()
        for entry in self.registry.entries:
            self._validate_entry(entry, result)
            if entry.id in ids_seen:
                result.add_error(f"duplicate skill id: {entry.id}")
            ids_seen.add(entry.id)
        return result

    def validate_one(self, skill_id: str) -> ValidationResult:
        result = ValidationResult(ok=True)
        entry = self.registry.get(skill_id)
        if not entry:
            result.add_error(f"skill not found: {skill_id}")
            return result
        self._validate_entry(entry, result)
        return result

    # ---- internals -------------------------------------------------------

    def _validate_entry(self, entry: SkillEntry, result: ValidationResult) -> None:
        # Path exists
        skill_dir = self.skills_root / Path(*entry.path.split("/"))
        if not skill_dir.exists():
            result.add_error(f"[{entry.id}] skill path does not exist: {skill_dir}")
            return
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            result.add_error(f"[{entry.id}] SKILL.md missing at {skill_md}")
            return
        try:
            text = skill_md.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"[{entry.id}] cannot read SKILL.md: {e}")
            return
        # Frontmatter sanity
        if not text.startswith("---"):
            result.add_error(f"[{entry.id}] SKILL.md is missing YAML frontmatter")
        else:
            from .frontmatter import parse_frontmatter
            meta, _ = parse_frontmatter(text)
            for k in REQUIRED_FRONTMATTER:
                if k not in meta or not meta[k]:
                    result.add_error(f"[{entry.id}] required frontmatter key missing or empty: {k}")
            if meta.get("name") != entry.name:
                result.add_error(f"[{entry.id}] frontmatter name does not match registry")
            if meta.get("category") != entry.category:
                result.add_error(f"[{entry.id}] frontmatter category does not match registry")
        headings = {m.group(1).strip().lower() for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)}
        for section in sorted(REQUIRED_SECTIONS):
            if section.lower() not in headings:
                result.add_error(f"[{entry.id}] required section missing: {section}")
        expected_path = f"{entry.category}/{entry.name}"
        if entry.path != expected_path:
            result.add_error(f"[{entry.id}] path must be {expected_path}, got {entry.path}")
        for target in entry.composes_with + entry.suggests_after:
            if not self.registry.get(target):
                result.add_error(f"[{entry.id}] composition target not found: {target}")
        # Scan every readable skill file. Third-party scripts are never executed.
        for f in skill_dir.rglob("*"):
            if not f.is_file() or f.stat().st_size > 2_000_000:
                continue
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            for pattern, label in SUSPICIOUS_PATTERNS:
                if pattern.search(content):
                    result.add_warning(f"[{entry.id}] {f.relative_to(skill_dir)} contains suspicious pattern: {label}")
        if not (skill_dir / "README.md").exists():
            result.add_error(f"[{entry.id}] README.md missing")
        source_repository = meta.get("source_repository") if text.startswith("---") else None
        if source_repository:
            for key in ("source_path", "source_commit", "license", "original_author"):
                if not meta.get(key):
                    result.add_error(f"[{entry.id}] imported skill metadata missing: {key}")
            if not (skill_dir / "LICENSE").exists():
                result.add_error(f"[{entry.id}] imported skill LICENSE missing")
            if not (skill_dir / "references" / "upstream-SKILL.md").exists():
                result.add_error(f"[{entry.id}] upstream SKILL reference missing")