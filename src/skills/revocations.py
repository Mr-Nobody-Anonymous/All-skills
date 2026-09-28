"""Single source of truth for revoked and quarantined skills.

Every consumer — the router, the execution runtime and the quarantine workflow
in :mod:`skills.security` — reads and writes revocations through this module,
so quarantining a skill is guaranteed to stop it from being routed or executed.

Contract (``registry/revocations.json``)::

    {
      "version": "1.0.0",
      "revoked_skills": [
        {"id": "<skill id>", "reason": "...", "revoked_at": "<ISO-8601>",
         "severity": "low|medium|high|critical", "advisory_id": null,
         "replacement": null, "reporter": "..."}
      ]
    }

For backwards compatibility the reader also accepts the legacy shapes written
by earlier releases: a ``revoked_skills`` mapping of ``id -> details`` and the
``revocations`` list (with ``skill_id``) that ``quarantine_skill()`` wrote to
``skills/revocations.json``. Legacy entries remain in force until removed.

Invalid data fails closed: :class:`RevocationError` is raised instead of
silently treating the kill-switch registry as empty.
"""
from __future__ import annotations

import json
import os
import tempfile
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

REVOCATIONS_RELPATH = Path("registry") / "revocations.json"
LEGACY_RELPATH = Path("skills") / "revocations.json"
SEVERITIES = ("low", "medium", "high", "critical")
_DEFAULT_REASON = "Revoked by security policy"


class RevocationError(RuntimeError):
    """The revocation registry exists but cannot be trusted (unreadable or malformed)."""


@dataclass(frozen=True)
class Revocation:
    id: str
    reason: str = _DEFAULT_REASON
    revoked_at: str = ""
    severity: str = "high"
    advisory_id: Optional[str] = None
    replacement: Optional[str] = None
    reporter: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def revocations_path(repo_root: Path) -> Path:
    return Path(repo_root) / REVOCATIONS_RELPATH


def _parse_entry(raw: Any, fallback_id: Optional[str], source: Path) -> Revocation:
    if not isinstance(raw, dict):
        raise RevocationError(f"{source}: revocation entry must be an object, got {type(raw).__name__}")
    skill_id = raw.get("id") or raw.get("skill_id") or fallback_id
    if not isinstance(skill_id, str) or not skill_id.strip():
        raise RevocationError(f"{source}: revocation entry without a skill id: {raw!r}")
    reason = raw.get("reason", _DEFAULT_REASON)
    if not isinstance(reason, str):
        raise RevocationError(f"{source}: revocation reason for '{skill_id}' must be a string")
    severity = str(raw.get("severity", "high")).strip().lower()
    return Revocation(
        id=skill_id.strip(),
        reason=reason or _DEFAULT_REASON,
        revoked_at=str(raw.get("revoked_at") or ""),
        severity=severity if severity in SEVERITIES else "high",
        advisory_id=raw.get("advisory_id"),
        replacement=raw.get("replacement"),
        reporter=raw.get("reporter"),
    )


def load_revocations(path: Path) -> Dict[str, Revocation]:
    """Parse one revocations file. A missing file means "nothing revoked"."""
    path = Path(path)
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise RevocationError(f"{path}: unreadable revocation registry: {exc}") from exc
    if not isinstance(data, dict):
        raise RevocationError(f"{path}: revocation registry must be a JSON object")
    if "revoked_skills" in data:
        raw = data["revoked_skills"]
    elif "revocations" in data:
        raw = data["revocations"]
    else:
        raise RevocationError(f"{path}: missing 'revoked_skills' list")

    result: Dict[str, Revocation] = {}
    if isinstance(raw, list):
        for item in raw:
            rev = _parse_entry(item, None, path)
            result[rev.id] = rev
    elif isinstance(raw, dict):
        for key, item in raw.items():
            rev = _parse_entry(item if isinstance(item, dict) else {}, str(key), path)
            result[rev.id] = rev
    else:
        raise RevocationError(f"{path}: 'revoked_skills' must be a list, got {type(raw).__name__}")
    return result


def load_all(repo_root: Path) -> Dict[str, Revocation]:
    """Canonical registry merged with the legacy quarantine file, if present."""
    merged = load_revocations(Path(repo_root) / LEGACY_RELPATH)
    merged.update(load_revocations(revocations_path(repo_root)))
    return merged


def get_revocation(skill_id: str, repo_root: Path) -> Optional[Revocation]:
    return load_all(repo_root).get(skill_id)


def _read_document(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {
            "version": "1.0.0",
            "description": "Authoritative registry of revoked, compromised, or security-quarantined skills.",
            "revoked_skills": [],
        }
    load_revocations(path)  # validates; raises RevocationError on malformed data
    doc: Dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    return doc


def _canonical_entries(doc: Dict[str, Any], source: Path) -> List[Dict[str, Any]]:
    raw = doc.get("revoked_skills", doc.get("revocations", []))
    if isinstance(raw, dict):
        return [_parse_entry(v if isinstance(v, dict) else {}, str(k), source).to_dict() for k, v in raw.items()]
    return [_parse_entry(item, None, source).to_dict() for item in raw]


def _write_document(path: Path, doc: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".revocations-", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(doc, handle, indent=2)
            handle.write("\n")
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def add_revocation(
    repo_root: Path,
    skill_id: str,
    reason: str,
    *,
    severity: str = "high",
    reporter: Optional[str] = None,
    advisory_id: Optional[str] = None,
    replacement: Optional[str] = None,
) -> Revocation:
    """Revoke ``skill_id`` in ``registry/revocations.json`` (idempotent)."""
    path = revocations_path(repo_root)
    doc = _read_document(path)
    entries = _canonical_entries(doc, path)
    now = datetime.now(timezone.utc)
    rev = Revocation(
        id=skill_id,
        reason=reason or _DEFAULT_REASON,
        revoked_at=now.isoformat(timespec="seconds").replace("+00:00", "Z"),
        severity=severity if severity in SEVERITIES else "high",
        advisory_id=advisory_id,
        replacement=replacement,
        reporter=reporter,
    )
    if not any(e["id"] == skill_id for e in entries):
        entries.append(rev.to_dict())
    doc.pop("revocations", None)
    doc["revoked_skills"] = entries
    doc["last_updated"] = now.date().isoformat()
    _write_document(path, doc)
    return next(Revocation(**e) for e in entries if e["id"] == skill_id)


def remove_revocation(repo_root: Path, skill_id: str) -> bool:
    """Lift a revocation from the canonical and the legacy file. Returns True if removed."""
    removed = False
    for path in (revocations_path(repo_root), Path(repo_root) / LEGACY_RELPATH):
        if not path.exists():
            continue
        doc = _read_document(path)
        entries = _canonical_entries(doc, path)
        kept = [e for e in entries if e["id"] != skill_id]
        if len(kept) != len(entries):
            removed = True
            doc.pop("revocations", None)
            doc["revoked_skills"] = kept
            doc["last_updated"] = datetime.now(timezone.utc).date().isoformat()
            _write_document(path, doc)
    return removed
