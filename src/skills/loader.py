"""Loader for individual SKILL.md files and skill folders."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Dict, List, Optional

from .frontmatter import parse_frontmatter
from .registry import SkillEntry


@dataclass
class LoadedSkill:
    entry: SkillEntry
    skill_md_path: Path
    body: str
    files: List[str]


class Loader:
    def __init__(self, skills_root: Path) -> None:
        self.skills_root = skills_root

    def resolve_path(self, skill_id: str) -> Optional[Path]:
        """Resolve a canonical skill ID without permitting traversal or quarantine access."""
        parts = skill_id.split(".")
        if len(parts) != 2 or any(not re.fullmatch(r"[a-z0-9][a-z0-9-]*", part) for part in parts):
            return None
        if "_quarantine" in parts:
            return None
        return self.skills_root.joinpath(*parts)

    def load(self, skill_id: str) -> Optional[LoadedSkill]:
        skill_dir = self.resolve_path(skill_id)
        if not skill_dir or not skill_dir.exists():
            return None
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            return None
        return _load_skill_file(skill_id, skill_md, skill_dir)


def load_skill(skills_root: Path, skill_id: str) -> Optional[LoadedSkill]:
    return Loader(skills_root).load(skill_id)


def _load_skill_file(skill_id: str, skill_md: Path, skill_dir: Path) -> Optional[LoadedSkill]:
    try:
        text = skill_md.read_text(encoding="utf-8")
    except Exception:
        return None
    meta, body = parse_frontmatter(text)
    if not meta:
        return None
    # Build entry from frontmatter
    rel = str(skill_dir.relative_to(skill_dir.parent.parent)).replace("\\", "/")
    entry = SkillEntry(
        id=meta.get("id", skill_id),
        name=meta.get("name", skill_dir.name),
        category=meta.get("category", skill_dir.parts[-2] if len(skill_dir.parts) >= 2 else "utilities"),
        description=meta.get("description", ""),
        path=rel,
        aliases=meta.get("aliases", []) or [],
        triggers=meta.get("triggers", []) or [],
        keywords=meta.get("keywords", []) or [],
        dependencies=meta.get("dependencies", []) or [],
        composes_with=meta.get("composes_with", []) or [],
        suggests_after=meta.get("suggests_after", []) or [],
        source=meta.get("source"),
        enabled=str(meta.get("enabled", "true")).lower() not in {"false", "no", "0", "off"},
        risk=meta.get("risk", "low"),
        version=meta.get("version", "1.0.0"),
    )
    files = sorted([p.name for p in skill_dir.rglob("*") if p.is_file()])
    return LoadedSkill(entry=entry, skill_md_path=skill_md, body=body, files=files)