"""Evidence-based trust tiers and provenance verification.

Nothing is trusted by default. A skill's tier is the highest rung of the
ladder whose evidence is actually present:

=================  ==========================================================
``T0_UNKNOWN``     Not found, quarantined, or its SKILL.md does not parse.
``T1_DISCOVERED``  SKILL.md exists and declares a name and description.
``T2_SCANNED``     The static security scan completed (no unscannable or
                   unreadable files) and found no high-severity issue.
``T3_REVIEWED``    A maintainer review record exists in ``registry/trust.json``
                   and was made against the skill's *current* content hash.
``T4_TESTED``      The review record lists tests/evals that exist.
``T5_CURATED``     Granted in the trust ledger on top of T3 + T4 evidence.
``T6_PRODUCTION``  Granted in the trust ledger on top of T3 + T4 evidence.
=================  ==========================================================

The ledger is maintained by humans; any edit to a skill changes its content
hash and automatically invalidates the review (the skill falls back to T2).
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .frontmatter import parse_frontmatter
from .lock import compute_skill_tree_hash
from .registry import SkillEntry, TrustTier

TRUST_LEDGER_RELPATH = Path("registry") / "trust.json"


class TrustLedgerError(ValueError):
    """``registry/trust.json`` exists but is malformed."""


@dataclass
class TrustAssessment:
    skill_id: str
    tier: TrustTier
    evidence: Dict[str, Any] = field(default_factory=dict)
    reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {"skill_id": self.skill_id, "tier": self.tier.name, "evidence": self.evidence, "reasons": self.reasons}


def load_trust_ledger(workspace_root: Path) -> Dict[str, Dict[str, Any]]:
    """Maintainer review records keyed by skill id (empty if the ledger does not exist)."""
    path = Path(workspace_root) / TRUST_LEDGER_RELPATH
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise TrustLedgerError(f"{path}: unreadable trust ledger: {exc}") from exc
    records = data.get("skills") if isinstance(data, dict) else None
    if not isinstance(records, dict) or not all(isinstance(v, dict) for v in records.values()):
        raise TrustLedgerError(f"{path}: 'skills' must map skill ids to review records")
    return records


def skill_directory(entry: SkillEntry, workspace_root: Path) -> Path:
    return Path(workspace_root) / "skills" / Path(*entry.path.split("/"))


def assess_trust(
    entry: Optional[SkillEntry],
    workspace_root: Path,
    ledger: Optional[Dict[str, Dict[str, Any]]] = None,
) -> TrustAssessment:
    """Compute the evidence-backed trust tier of ``entry``."""
    if entry is None:
        return TrustAssessment("", TrustTier.T0_UNKNOWN, reasons=["skill not found"])
    result = TrustAssessment(entry.id, TrustTier.T0_UNKNOWN)
    if (entry.lifecycle or "").strip().lower() == "quarantined":
        result.reasons.append("skill is quarantined")
        return result

    skill_dir = skill_directory(entry, workspace_root)
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        result.reasons.append(f"missing {skill_md}")
        return result
    meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8", errors="replace"))
    if not meta.get("name") or not meta.get("description"):
        result.reasons.append("SKILL.md frontmatter lacks name/description")
        return result
    result.tier = TrustTier.T1_DISCOVERED

    from .security import apply_allowlist, load_allowlist, scan_is_complete, scan_skill

    findings = scan_skill(entry, skill_dir)
    # Maintainer-reviewed exceptions apply to findings, never to incomplete scans.
    active, suppressed, _ = apply_allowlist(findings, load_allowlist(workspace_root), {entry.id: skill_dir})
    high = [f for f in active if f.severity == "high"]
    complete = scan_is_complete(findings)
    result.evidence["security_scan"] = {
        "complete": complete,
        "high_findings": len(high),
        "warnings": sum(1 for f in active if f.severity == "warn"),
        "suppressed_by_allowlist": len(suppressed),
    }
    if not complete:
        result.reasons.append("security scan incomplete (unscannable or unreadable files)")
        return result
    if high:
        result.reasons.append(f"{len(high)} high-severity security finding(s)")
        return result
    result.tier = TrustTier.T2_SCANNED

    records = load_trust_ledger(workspace_root) if ledger is None else ledger
    record = records.get(entry.id)
    if not record:
        result.reasons.append("no maintainer review record in registry/trust.json")
        return result
    current_hash, _ = compute_skill_tree_hash(skill_dir)
    result.evidence["review"] = {
        "reviewed_by": record.get("reviewed_by"),
        "reviewed_at": record.get("reviewed_at"),
        "hash_matches": record.get("sha256") == current_hash,
    }
    if not record.get("reviewed_by") or record.get("sha256") != current_hash:
        result.reasons.append("review record is missing a reviewer or predates the current content")
        return result
    result.tier = TrustTier.T3_REVIEWED

    tests = [str(t) for t in record.get("tests", []) or []]
    existing = [t for t in tests if (Path(workspace_root) / t.split("::")[0]).exists()]
    result.evidence["tests"] = {"declared": tests, "existing": existing}
    if not tests or len(existing) != len(tests):
        result.reasons.append("review record lists no tests, or listed tests do not exist")
        return result
    result.tier = TrustTier.T4_TESTED

    granted = str(record.get("tier", "")).strip()
    if granted in ("T5_CURATED", "T6_PRODUCTION"):
        result.tier = TrustTier[granted]
    return result


def verify_provenance(entry: Optional[SkillEntry], workspace_root: Path) -> Dict[str, Any]:
    """Check a skill's content against ``skills.lock`` and its source record.

    ``verified`` is true only if the lockfile pins the skill, the current
    content hash matches the pinned hash, and a provenance record exists in
    ``skills/SOURCES.json``.
    """
    if entry is None:
        return {"verified": False, "error": "skill not found"}
    root = Path(workspace_root)
    reasons: List[str] = []

    lock_path = root / "skills.lock"
    locked: Dict[str, Any] = {}
    if lock_path.exists():
        locked = json.loads(lock_path.read_text(encoding="utf-8")).get("skills", {}).get(entry.id) or {}
    current_hash, _ = compute_skill_tree_hash(skill_directory(entry, root))
    hash_valid = bool(locked) and locked.get("sha256") == current_hash
    if not locked:
        reasons.append("skill is not pinned in skills.lock")
    elif not hash_valid:
        reasons.append("content does not match the hash pinned in skills.lock")

    source_record: Optional[Dict[str, Any]] = None
    sources_path = root / "skills" / "SOURCES.json"
    if sources_path.exists():
        records = json.loads(sources_path.read_text(encoding="utf-8")).get("skills", [])
        source_record = next((r for r in records if r.get("skill") == entry.id), None)
    if source_record is None:
        reasons.append("no provenance record in skills/SOURCES.json")

    return {
        "verified": hash_valid and source_record is not None,
        "skill_id": entry.id,
        "version": entry.version,
        "content_sha256": current_hash,
        "locked_sha256": locked.get("sha256"),
        "hash_valid": hash_valid,
        "source": (source_record or {}).get("repository") or (source_record or {}).get("source") or "unknown",
        "commit": (source_record or {}).get("commit"),
        "license": (source_record or {}).get("license"),
        "reasons": reasons,
    }
