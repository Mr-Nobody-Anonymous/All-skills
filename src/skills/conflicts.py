"""Declared and semantic skill conflicts & automated resolution.

Handles mutually exclusive capabilities, conflicting architectural paradigms (e.g.
Prisma vs Drizzle, Tailwind vs CSS modules, NextAuth vs Clerk), and applies a deterministic
priority resolution hierarchy:
  1. Project configuration (explicit workspace config / package.json)
  2. User prompt preference (explicit keyword in query)
  3. Trusted official canonical suite (Tier 1 vs generic)
  4. Higher empirical quality score
  5. Specificity to the target capability slot
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .registry import Registry, SkillEntry


@dataclass(frozen=True)
class ConflictRecord:
    skills: List[str] = field(default_factory=list)
    reason: str = ""
    severity: str = "warn"  # info | warn | error
    priority: str = ""


# Known semantic conflict domains where skills cannot be safely co-activated
SEMANTIC_CONFLICT_GROUPS: List[Dict[str, Any]] = [
    {
        "domain": "typescript_orm",
        "description": "Mutually exclusive TypeScript database abstraction layers",
        "skills": ["prisma-expert", "drizzle-orm-expert", "typeorm", "sequelize"],
        "default_priority": "drizzle-orm-expert",
    },
    {
        "domain": "react_state_management",
        "description": "Conflicting primary global client state management paradigms",
        "skills": ["redux-toolkit", "zustand", "jotai", "mobx"],
        "default_priority": "zustand",
    },
    {
        "domain": "e2e_testing",
        "description": "Redundant parallel end-to-end browser automation frameworks",
        "skills": ["playwright-skill", "cypress", "puppeteer"],
        "default_priority": "playwright-skill",
    },
    {
        "domain": "database_engine",
        "description": "Conflicting primary relational vs document store persistence models",
        "skills": ["postgresql-optimization-tuning", "mongodb-aggregation-sharding"],
        "default_priority": "postgresql-optimization-tuning",
    },
    {
        "domain": "payment_processors",
        "description": "Conflicting primary checkout payment providers",
        "skills": ["stripe", "paypal", "paddle", "fintech-payment-gateways"],
        "default_priority": "stripe",
    },
]


class ConflictResolver:
    """Detects and resolves semantic and declared conflicts between candidate skills."""

    def __init__(self, conflict_store: Optional[ConflictStore] = None) -> None:
        self.conflict_store = conflict_store or ConflictStore([])
        self.semantic_groups = SEMANTIC_CONFLICT_GROUPS

    def detect_conflicts(self, skill_ids: List[str]) -> List[Dict[str, Any]]:
        """Identify all conflict pairs among a candidate list of skills."""
        detected: List[Dict[str, Any]] = []
        skill_set = set(skill_ids)

        # 1. Check explicit conflict store records
        for c in self.conflict_store.all():
            matching = [s for s in c.skills if s in skill_set]
            if len(matching) >= 2:
                detected.append({
                    "type": "declared",
                    "skills": matching,
                    "reason": c.reason,
                    "severity": c.severity,
                    "priority": c.priority,
                })

        # 2. Check semantic conflict groups
        for g in self.semantic_groups:
            group_skills = g["skills"]
            matching = [s for s in skill_ids if any(s == gs or gs in s for gs in group_skills)]
            if len(matching) >= 2:
                detected.append({
                    "type": "semantic",
                    "domain": g["domain"],
                    "skills": matching,
                    "description": g["description"],
                    "default_priority": g.get("default_priority"),
                })

        return detected

    def resolve(
        self,
        candidate_skills: List[str],
        user_preferences: Optional[Set[str]] = None,
        project_config: Optional[Dict[str, Any]] = None,
        skill_quality_scores: Optional[Dict[str, float]] = None,
    ) -> Tuple[List[str], List[Dict[str, Any]]]:
        """Resolve all conflicts, returning the filtered list of skills and resolution explanations."""
        prefs = user_preferences or set()
        p_cfg = project_config or {}
        scores = skill_quality_scores or {}

        resolved_skills = list(candidate_skills)
        resolutions = []

        conflicts = self.detect_conflicts(resolved_skills)
        for conf in conflicts:
            conflicting = conf["skills"]
            # Find the winner according to resolution hierarchy:
            # 1. Project config
            winner = None
            rule_applied = None

            for s in conflicting:
                if s in p_cfg.get("skills", []) or any(dep in p_cfg.get("dependencies", {}) for dep in [s]):
                    winner = s
                    rule_applied = "project configuration"
                    break

            # 2. User prompt preference
            if not winner:
                for s in conflicting:
                    if any(pref in s.lower() for pref in prefs):
                        winner = s
                        rule_applied = "explicit user prompt preference"
                        break

            # 3. Explicit priority or default priority
            if not winner:
                prio = conf.get("priority") or conf.get("default_priority")
                if prio and prio in conflicting:
                    winner = prio
                    rule_applied = "canonical platform default priority"

            # 4. Quality score comparison
            if not winner:
                scored = sorted(conflicting, key=lambda s: scores.get(s, 5.0), reverse=True)
                winner = scored[0]
                rule_applied = f"higher quality score ({scores.get(winner, 5.0):.1f})"

            # Remove losers
            for s in conflicting:
                if s != winner and s in resolved_skills:
                    resolved_skills.remove(s)
                    resolutions.append({
                        "description": conf.get("description") or conf.get("reason") or "Skill conflict",
                        "resolution_rule": rule_applied,
                        "winner": winner,
                        "loser": s,
                    })

        return resolved_skills, resolutions


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
