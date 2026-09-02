"""Declared skill conflicts.

``skills/conflicts.json`` lists pairs of skills that should not run
simultaneously, with a severity and a priority. The validator reports active
conflicts; future routers can use the priority to break ties.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .registry import Registry


@dataclass(frozen=True)
class ConflictRecord:
    skills: List[str] = field(default_factory=list)
    reason: str = ""
    severity: str = "warn"  # info | warn | error
    priority: str = ""


class ConflictStore:
    """In-memory index of declared conflicts."""

    def __init__(self, conflicts: List[ConflictRecord]) -> None:
        self.conflicts = conflicts

    @classmethod
    def load(cls, path: Path) -> "ConflictStore":
        if not path.exists():
            return cls([])
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return cls([])
        conflicts: List[ConflictRecord] = []
        for raw in data.get("conflicts", []):
            skills = [str(s).strip() for s in raw.get("skills", []) if str(s).strip()]
            if len(skills) < 2:
                continue
            conflicts.append(
                ConflictRecord(
                    skills=skills,
                    reason=str(raw.get("reason") or ""),
                    severity=str(raw.get("severity") or "warn").strip().lower(),
                    priority=str(raw.get("priority") or "").strip(),
                )
            )
        return cls(conflicts)

    def all(self) -> List[ConflictRecord]:
        return list(self.conflicts)

    def active(self, registry: Registry) -> List[ConflictRecord]:
        """Conflicts where every referenced skill exists and is enabled."""
        active: List[ConflictRecord] = []
        for conflict in self.conflicts:
            entries = [registry.get(skill_id) for skill_id in conflict.skills]
            if all(entry is not None and entry.enabled for entry in entries):
                active.append(conflict)
        return active


def load_conflicts(workspace_root: Path) -> ConflictStore:
    """Load declared conflicts from ``<workspace_root>/skills/conflicts.json``."""
    return ConflictStore.load(workspace_root / "skills" / "conflicts.json")