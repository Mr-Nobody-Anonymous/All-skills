"""Skill quality scoring.

Deterministic, dependency-free heuristics that score a skill from 0-10 across
six axes (documentation, maintenance, reliability, security, compatibility,
usefulness) using only data already present in the skill's SKILL.md and the
registry. An ``overall_score`` (weighted average) lets the router prefer a
well-documented, maintained, low-risk skill over a sparse one with identical
keywords.

The scores are advisory signals, not judgments about a skill's content. They are
stored in ``registry.json`` under ``quality`` so the router, ``doctor``, and any
UI can all use the exact same numbers.
"""
from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Dict, Optional

from .registry import Registry, SkillEntry

AXES = (
    "documentation",
    "maintenance",
    "reliability",
    "security",
    "compatibility",
    "usefulness",
)

# Weights used for the overall weighted-average score.
WEIGHTS: Dict[str, float] = {
    "documentation": 0.20,
    "maintenance": 0.15,
    "reliability": 0.20,
    "security": 0.20,
    "compatibility": 0.10,
    "usefulness": 0.15,
}

REQUIRED_SECTIONS = (
    "Purpose", "When to Use", "When NOT to Use", "Capabilities", "Inputs",
    "Workflow", "Tools", "Examples", "Safety", "Source", "Notes",
)

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+")
_HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.MULTILINE)


@dataclass
class QualityReport:
    skill_id: str
    documentation: float = 0.0
    maintenance: float = 0.0
    reliability: float = 0.0
    security: float = 0.0
    compatibility: float = 0.0
    usefulness: float = 0.0
    overall_score: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)


def _cap(value: float, hi: float = 10.0) -> float:
    return max(0.0, min(value, hi))


def score_entry(entry: SkillEntry, skill_dir: Optional[Path] = None) -> QualityReport:
    """Score a single skill from its registry entry and optional on-disk folder."""
    body = _read_body(skill_dir)
    headings = set(_HEADING_RE.findall(body.replace("\r", ""))) if body else set()
    headings_l = {h.strip().lower() for h in headings}
    report = QualityReport(skill_id=entry.id)

    # ---- documentation -------------------------------------------------
    doc = 1.0
    desc = (entry.description or "").strip()
    if desc:
        doc += min(len(desc) / 40.0, 3.0)
    present = sum(1 for s in REQUIRED_SECTIONS if s.lower() in headings_l)
    doc += (present / len(REQUIRED_SECTIONS)) * 3.0
    if skill_dir is not None and (skill_dir / "README.md").exists():
        doc += 2.0
    report.documentation = round(_cap(doc), 1)

    # ---- maintenance ---------------------------------------------------
    maint = 0.0
    if entry.version and SEMVER_RE.match(entry.version or ""):
        maint += 3.0
    if entry.source:
        maint += 2.0
    if entry.source and str(entry.source) not in ("custom", "None", "null"):
        maint += 2.0  # imported provenance (recorded repository)
    if str(entry.source or "custom") not in ("custom",) and skill_dir is not None:
        if (skill_dir / "LICENSE").exists():
            maint += 1.5
        if (skill_dir / "references" / "upstream-SKILL.md").exists():
            maint += 1.5
    report.maintenance = round(_cap(maint), 1)

    # ---- reliability ---------------------------------------------------
    rel = (present / len(REQUIRED_SECTIONS)) * 5.0
    rel += 2.0 if entry.dependencies is not None else 0.0
    if skill_dir is not None:
        has_scripts = (skill_dir / "scripts").exists() or any(
            p.suffix in {".py", ".mjs", ".js", ".ts", ".sh"} and p.name != "SKILL.md"
            for p in skill_dir.rglob("*")
            if p.is_file()
        )
        if has_scripts:
            rel += 2.0
    if entry.composes_with or entry.suggests_after:
        rel += 1.0
    report.reliability = round(_cap(rel), 1)

    # ---- security ------------------------------------------------------
    risk = (entry.risk or "low").strip().lower()
    sec = {"low": 9.0, "medium": 6.0, "high": 3.0}.get(risk, 5.0)
    perms = entry.permissions or {}
    if perms and all(str(v).strip().lower() in {"none", "read"} for v in perms.values()):
        sec = min(sec + 0.5, 10.0)
    report.security = round(sec, 1)

    # ---- compatibility -------------------------------------------------
    comp = 4.0  # the open Agent Skills SKILL.md convention is agent-agnostic by default
    compat = entry.compatibility or {}
    if compat:
        comp += 3.0 if compat.get("generic") in (True, "true", "True", "yes") else 2.0
        known_true = sum(
            1 for k, v in compat.items()
            if k not in ("generic",) and v in (True, "true", "True", "yes")
        )
        comp += min(known_true, 3) * 1.0
    report.compatibility = round(_cap(comp), 1)

    # ---- usefulness ----------------------------------------------------
    useful = min(len(entry.keywords) / 5.0, 3.0)
    useful += min(len(entry.triggers) / 5.0, 3.0)
    useful += min(len(entry.aliases) / 3.0, 2.0)
    useful += min(len(entry.capabilities) / 5.0, 2.0)
    report.usefulness = round(_cap(useful), 1)

    overall = sum(getattr(report, axis) * WEIGHTS[axis] for axis in AXES)
    report.overall_score = round(overall, 1)
    return report


def score_all(registry: Registry, skills_root: Path) -> Dict[str, QualityReport]:
    """Score every skill in the registry against its on-disk folder."""
    reports: Dict[str, QualityReport] = {}
    for entry in registry.entries:
        skill_dir = skills_root / Path(*entry.path.split("/"))
        reports[entry.id] = score_entry(entry, skill_dir)
    return reports


def _read_body(skill_dir: Optional[Path]) -> str:
    if skill_dir is None:
        return ""
    try:
        from .frontmatter import parse_frontmatter

        text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
        return parse_frontmatter(text)[1]
    except Exception:
        return ""