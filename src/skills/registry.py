"""Skill registry — loads and queries the central index of skills."""
from __future__ import annotations

import json
import os
from dataclasses import dataclass, field, asdict as dc_asdict
from enum import IntEnum
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


class TrustTier(IntEnum):
    """The T0-T6 progressive Trust Ladder for All-Skills platform."""
    T0_UNKNOWN = 0
    T1_DISCOVERED = 1
    T2_SCANNED = 2
    T3_REVIEWED = 3
    T4_TESTED = 4
    T5_CURATED = 5
    T6_PRODUCTION = 6


@dataclass
class SkillIdentity:
    """Formal multi-dimensional identity model separating trust from catalog availability."""
    id: str
    version: str
    schema_version: str = "1.0.0"
    source: Dict[str, Any] = field(default_factory=dict)
    # Conservative defaults: nothing is trusted until evidence says otherwise.
    trust_tier: TrustTier = TrustTier.T0_UNKNOWN
    trust_status: str = "unverified"
    availability: str = "catalog"
    review_status: str = "not_reviewed"
    security_status: str = "not_scanned"
    behavior_status: str = "not_evaluated"
    production_status: str = "not_approved"
    capabilities: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    permissions: Dict[str, Any] = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)
    side_effects: List[str] = field(default_factory=list)
    platforms: List[str] = field(default_factory=list)
    tests: List[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        d = dc_asdict(self)
        d["trust_tier"] = self.trust_tier.name
        return d


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
    # Lifecycle: discovered | imported | validated | security_scanned | ready |
    # enabled | disabled | quarantined | deprecated
    lifecycle: str = "enabled"
    capabilities: List[str] = field(default_factory=list)
    forbidden: List[str] = field(default_factory=list)
    # Evidence-derived tier (see skills.trust); unknown until assessed.
    trust_tier: str = "T0_UNKNOWN"
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    permissions: Optional[Dict[str, str]] = None
    compatibility: Optional[Dict[str, Any]] = None
    quality: Optional[Dict[str, float]] = None
    quality_score: float = 0.0

    def to_dict(self) -> dict:
        d = dc_asdict(self)
        for key in ("permissions", "compatibility", "quality"):
            if d.get(key) is None:
                d[key] = {}
        if not d.get("quality"):
            d["quality"] = {}
        if d.get("quality_score") is None:
            d["quality_score"] = 0.0
        return d

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
        clean.setdefault("lifecycle", "enabled")
        clean.setdefault("capabilities", [])
        clean.setdefault("forbidden", [])
        clean.setdefault("trust_tier", "T0_UNKNOWN")
        clean.setdefault("inputs", [])
        clean.setdefault("outputs", [])
        clean.setdefault("permissions", None)
        clean.setdefault("compatibility", None)
        clean.setdefault("quality", None)
        clean.setdefault("quality_score", 0.0)
        return cls(**clean)


class Registry:
    """In-memory index of skills. Built from registry.json + on-disk SKILL.md files."""

    def __init__(self, entries: Optional[List[SkillEntry]] = None) -> None:
        self.entries: List[SkillEntry] = entries or []
        # Set by Registry.load(); needed for evidence checks (trust, provenance).
        self.workspace_root: Optional[Path] = None

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
            except Exception as e:
                # Corrupted registry — fail closed in production
                raise ValueError(
                    f"Corrupted or invalid registry file '{registry_path}': {e}. "
                    "Fail-closed policy requires repairing or rebuilding the registry."
                ) from e
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
                id=str(meta["name"]) if meta.get("name") and "." in str(meta.get("name")) else sid_guess,
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
                lifecycle=meta.get("lifecycle", "enabled"),
                capabilities=meta.get("capabilities", []) or [],
                inputs=meta.get("inputs", []) or [],
                outputs=meta.get("outputs", []) or [],
                permissions=meta.get("permissions"),
                compatibility=meta.get("compatibility"),
                quality=meta.get("quality"),
                quality_score=float(meta.get("quality_score", 0.0) or 0.0),
            )
            reg.entries.append(entry)
            existing_ids.add(entry.id)
        reg.workspace_root = skills_root.parent
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

    def get_trust_tier(self, skill_id: str) -> TrustTier:
        """The recorded (evidence-derived) tier. Missing or invalid values are T0_UNKNOWN.

        ``scripts/refresh_registry.py`` computes this field from evidence and
        CI verifies it, so a hand-edited promotion fails the build.
        """
        entry = self.get(skill_id)
        if not entry or entry.lifecycle == "quarantined":
            return TrustTier.T0_UNKNOWN
        raw_tier = getattr(entry, "trust_tier", "")
        if isinstance(raw_tier, str) and raw_tier in TrustTier.__members__:
            return TrustTier[raw_tier]
        return TrustTier.T0_UNKNOWN

    def get_identity(self, skill_id: str) -> Optional[SkillIdentity]:
        entry = self.get(skill_id)
        if not entry:
            return None
        evidence: Dict[str, Any] = {}
        if self.workspace_root is not None:
            from .trust import assess_trust

            assessment = assess_trust(entry, self.workspace_root)
            tier, evidence = assessment.tier, assessment.evidence
        else:
            tier = self.get_trust_tier(skill_id)
        scan = evidence.get("security_scan")
        if not scan:
            security_status = "not_scanned"
        elif not scan["complete"]:
            security_status = "incomplete"
        else:
            security_status = "findings" if scan["high_findings"] else "scanned_clean"
        quarantined = entry.lifecycle == "quarantined"
        return SkillIdentity(
            id=entry.id,
            version=entry.version,
            source={"source": entry.source} if entry.source else {},
            trust_tier=tier,
            trust_status="quarantined" if quarantined else ("verified" if tier >= TrustTier.T4_TESTED else "unverified"),
            availability="active" if entry.enabled else "catalog",
            review_status="reviewed" if tier >= TrustTier.T3_REVIEWED else "not_reviewed",
            security_status=security_status,
            behavior_status="tested" if tier >= TrustTier.T4_TESTED else "not_evaluated",
            production_status="approved" if tier >= TrustTier.T6_PRODUCTION else "not_approved",
            capabilities=list(entry.capabilities),
            forbidden=list(entry.forbidden),
            permissions=dict(entry.permissions or {}),
            dependencies=list(entry.dependencies),
            side_effects=[],
            platforms=["claude", "cursor", "codex", "gemini", "antigravity", "openclaw"],
            tests=[],
        )

    def filter_by_trust(self, min_tier: TrustTier) -> List[SkillEntry]:
        return [e for e in self.entries if self.get_trust_tier(e.id) >= min_tier]

    def verify_provenance(self, skill_id: str) -> Dict[str, Any]:
        """Verify content against skills.lock and the source record (see skills.trust)."""
        entry = self.get(skill_id)
        if not entry:
            return {"verified": False, "error": f"Skill '{skill_id}' not found"}
        if self.workspace_root is None:
            return {"verified": False, "skill_id": entry.id, "error": "workspace unknown; load the registry with load_registry()"}
        from .trust import verify_provenance

        result = verify_provenance(entry, self.workspace_root)
        result["trust_tier"] = self.get_trust_tier(skill_id).name
        return result

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