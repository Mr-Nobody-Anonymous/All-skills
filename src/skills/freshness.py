"""Continuous Skill Freshness & Technology Drift Engine.

Monitors skill age, last verification timestamps, and checks for technology drift
(e.g., deprecated APIs, legacy versions, breaking library changes).
Classifies skills into 4 visual freshness tiers:
  🟢 Fresh  (<30 days)
  🟡 Stable (30–90 days)
  🟠 Aging  (90–180 days)
  🔴 Stale  (>180 days)
"""
from __future__ import annotations

import datetime
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .registry import Registry, SkillEntry


@dataclass
class FreshnessReport:
    """Freshness and drift assessment for a skill."""
    skill_id: str
    last_verified_date: str
    days_since_update: int
    tier: str                     # 'fresh' | 'stable' | 'aging' | 'stale'
    tier_symbol: str              # 🟢 | 🟡 | 🟠 | 🔴
    score: float                  # 0.0 to 100.0
    drift_detected: bool
    drift_warnings: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# Technology patterns that indicate legacy or deprecated practices
LEGACY_PATTERNS: List[Tuple[re.Pattern, str]] = [
    (re.compile(r"\bcomponentWillMount\b", re.I), "React legacy lifecycle componentWillMount detected"),
    (re.compile(r"\bcomponentWillReceiveProps\b", re.I), "React legacy lifecycle componentWillReceiveProps detected"),
    (re.compile(r"\bReactDOM\.render\(", re.I), "Legacy ReactDOM.render syntax; modern React uses createRoot"),
    (re.compile(r"\bvar\s+[a-zA-Z_]", re.I), "Legacy JavaScript 'var' keyword; modern code uses const/let"),
    (re.compile(r"\bpython\s+2(?:\.[0-9])?\b", re.I), "Python 2 references; deprecated and unsupported"),
    (re.compile(r"\bsetup\.py\s+(?:build|install)\b", re.I), "Deprecated setup.py direct invocation; modern builds use pyproject.toml / pip"),
    (re.compile(r"\bnode\s+(?:10|12|14)\b", re.I), "End-of-life Node.js runtime version referenced"),
]


class FreshnessEngine:
    """Calculates skill age and detects technology drift."""

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()

    def assess_skill(
        self,
        entry: SkillEntry,
        skill_dir: Optional[Path] = None,
        reference_date: Optional[datetime.date] = None,
    ) -> FreshnessReport:
        """Evaluate freshness and technology drift for a skill."""
        ref = reference_date or datetime.date.today()
        
        # Determine last verification date
        verified_date_str = "2026-09-20"
        if skill_dir is not None and (skill_dir / "SKILL.md").exists():
            try:
                mtime = (skill_dir / "SKILL.md").stat().st_mtime
                dt = datetime.date.fromtimestamp(mtime)
                verified_date_str = dt.isoformat()
            except Exception:
                pass

        try:
            skill_date = datetime.date.fromisoformat(verified_date_str)
            days = (ref - skill_date).days
            days = max(0, days)
        except Exception:
            days = 45

        # Classify tier
        if days < 30:
            tier = "fresh"
            symbol = "🟢"
            base_score = 98.0 - (days * 0.4)
        elif days <= 90:
            tier = "stable"
            symbol = "🟡"
            base_score = 86.0 - ((days - 30) * 0.25)
        elif days <= 180:
            tier = "aging"
            symbol = "🟠"
            base_score = 70.0 - ((days - 90) * 0.2)
        else:
            tier = "stale"
            symbol = "🔴"
            base_score = max(20.0, 50.0 - ((days - 180) * 0.1))

        # Check for technology drift
        drift_warnings = []
        body = ""
        if skill_dir is not None and (skill_dir / "SKILL.md").exists():
            try:
                body = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
            except Exception:
                pass

        for pattern, msg in LEGACY_PATTERNS:
            if pattern.search(body):
                drift_warnings.append(msg)

        drift_detected = len(drift_warnings) > 0
        final_score = max(0.0, base_score - (len(drift_warnings) * 12.0))

        return FreshnessReport(
            skill_id=entry.id,
            last_verified_date=verified_date_str,
            days_since_update=days,
            tier=tier,
            tier_symbol=symbol,
            score=round(final_score, 1),
            drift_detected=drift_detected,
            drift_warnings=drift_warnings,
        )

    def assess_all(
        self,
        registry: Registry,
        skills_root: Path,
    ) -> Dict[str, FreshnessReport]:
        """Assess all skills in the registry."""
        results = {}
        for entry in registry.entries:
            skill_dir = skills_root / Path(*entry.path.split("/"))
            results[entry.id] = self.assess_skill(entry, skill_dir)
        return results
