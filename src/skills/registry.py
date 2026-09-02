"""Skill registry — loads and queries the central index of skills."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict as dc_asdict
from pathlib import Path
from typing import Dict, Iterable, List, Optional


def _as_bool(value: object, default: bool = True) -> bool:
    """Coerce YAML-ish/JSON values without treating the string 'false' as true."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in {"true", "yes", "1", "on"}:
            return True
        if normalized in {"false", "no", "0", "off"}:
            return False
    if value is None:
        return default
    return bool(value)


@dataclass
class SkillEntry:
    id: str
    name: str
    category: str
    description: str
    path: str
    aliases: List[str] = field(default_factory=list)
    triggers: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    dependencies: List[str] = field(default_factory=list)
    composes_with: List[str] = field(default_factory=list)
    suggests_after: List[str] = field(default_factory=list)
    source: Optional[str] = None
    enabled: bool = True
    risk: str = "low"  # low | medium | high
    version: str = "1.0.0"

    def to_dict(self) -> dict:
        return dc_asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "SkillEntry":
        # Be tolerant of unknown fields
        known = {f for f in cls.__dataclass_fields__.keys()}
        clean = {k: v for k, v in d.items() if k in known}
        # Defaults for missing fields
        clean.setdefault("id", "")
        clean.setdefault("name", "")
        clean.setdefault("category", "utilities")
        clean.setdefault("description", "")
        clean.setdefault("path", "")
        clean.setdefault("aliases", [])
        clean.setdefault("triggers", [])
        clean.setdefault("keywords", [])
        clean.setdefault("dependencies", [])
        clean.setdefault("composes_with", [])
        clean.setdefault("suggests_after", [])
        clean.setdefault("source", None)
        clean["enabled"] = _as_bool(clean.get("enabled"), True)
        clean.setdefault("risk", "low")
        clean.setdefault("version", "1.0.0")
        return cls(**clean)


class Registry:
    """In-memory index of skills. Built from registry.json + on-disk SKILL.md files."""

    def __init__(self, entries: Optional[List[SkillEntry]] = None) -> None:
        self.entries: List[SkillEntry] = entries or []

    # ---- Loading ---------------------------------------------------------

    @classmethod
    def load(cls, registry_path: Path, skills_root: Path) -> "Registry":
        """Load registry from JSON file, falling back to scanning SKILL.md files."""
        reg = cls()
        if registry_path.exists():
            try:
                data = json.loads(registry_path.read_text(encoding="utf-8"))
                for raw in data.get("skills", []):
                    reg.entries.append(SkillEntry.from_dict(raw))
            except Exception:
                # Corrupted registry — fall back to disk scan
                pass
        # Merge entries from disk that are not already present
        existing_ids = {e.id for e in reg.entries}
        for skill_md in skills_root.rglob("SKILL.md"):
            if "_quarantine" in skill_md.parts:
                continue
            rel = skill_md.relative_to(skills_root).parent
            sid_guess = ".".join(rel.parts)
            if sid_guess in existing_ids:
                continue
            try:
                from .frontmatter import parse_frontmatter
                meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            except Exception:
                continue
            if not meta.get("name"):
                continue
            entry = SkillEntry(
                id=meta.get("name") if meta.get("name") and "." in str(meta.get("name")) else sid_guess,
                name=meta.get("name", rel.name),
                category=meta.get("category", rel.parts[0] if rel.parts else "utilities"),
                description=meta.get("description", ""),
                path=str(rel).replace(os.sep, "/"),
                aliases=meta.get("aliases", []) or [],
                triggers=meta.get("triggers", []) or [],
                keywords=meta.get("keywords", []) or [],
                dependencies=meta.get("dependencies", []) or [],
                composes_with=meta.get("composes_with", []) or [],
                suggests_after=meta.get("suggests_after", []) or [],
                source=meta.get("source"),
                enabled=_as_bool(meta.get("enabled"), True),
                risk=meta.get("risk", "low"),
                version=meta.get("version", "1.0.0"),
            )
            reg.entries.append(entry)
            existing_ids.add(entry.id)
        return reg

    # ---- Queries ---------------------------------------------------------

    def get(self, skill_id: str) -> Optional[SkillEntry]:
        for e in self.entries:
            if e.id == skill_id:
                return e
        return None

    def by_category(self, category: str) -> List[SkillEntry]:
        return [e for e in self.entries if e.category == category]

    def categories(self) -> Dict[str, int]:
        out: Dict[str, int] = {}
        for e in self.entries:
            out[e.category] = out.get(e.category, 0) + 1
        return out

    def search(self, query: str) -> List[SkillEntry]:
        q = query.lower().strip()
        if not q:
            return []
        results: List[SkillEntry] = []
        for e in self.entries:
            hay = " ".join(
                [e.id, e.name, e.description, e.category]
                + list(e.aliases)
                + list(e.triggers)
                + list(e.keywords)
            ).lower()
            if q in hay:
                results.append(e)
        return results

    def enabled(self) -> List[SkillEntry]:
        return [e for e in self.entries if e.enabled]

    def iter_all(self) -> Iterable[SkillEntry]:
        return iter(self.entries)

    # ---- Serialization ---------------------------------------------------

    def to_json(self) -> str:
        return json.dumps(
            {"version": 1, "skills": [e.to_dict() for e in self.entries]},
            indent=2,
        )


def load_registry(workspace_root: Path | None = None) -> Registry:
    """Convenience entry point."""
    root = workspace_root or Path.cwd()
    return Registry.load(
        registry_path=root / "skills" / "registry.json",
        skills_root=root / "skills",
    )