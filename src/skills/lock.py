"""Reproducible skill locking, cryptographic verification, and freshness tracking.

Implements deterministic SHA-256 tree hashing, lockfile generation (skills.lock),
cryptographic verification (skills verify), and freshness auditing (skills stale).
"""

from __future__ import annotations

import datetime
import hashlib
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def compute_file_sha256(file_path: Path) -> str:
    """Compute a platform-independent SHA-256 hex digest of a single file.

    Text files are hashed with normalised LF line endings so the digest is
    identical on Windows (``core.autocrlf`` CRLF checkouts) and POSIX systems;
    otherwise a lockfile generated on one OS reports every skill as "tampered"
    on another. Binary files (containing NUL bytes, the same heuristic Git
    uses) are hashed byte-for-byte.
    """
    data = file_path.read_bytes()
    if b"\0" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def compute_skill_tree_hash(skill_dir: Path) -> Tuple[str, List[str]]:
    """Compute deterministic SHA-256 hash across all files in a skill directory."""
    if not skill_dir.is_dir():
        return "", []

    file_entries: List[Tuple[str, str]] = []

    for path in skill_dir.rglob("*"):
        rel_parts = path.relative_to(skill_dir).parts
        # Skip dotfiles, hidden directories and interpreter caches so the hash
        # only reflects version-controlled skill content.
        if any(part.startswith(".") or part == "__pycache__" for part in rel_parts):
            continue
        if path.is_file():
            file_entries.append(("/".join(rel_parts), compute_file_sha256(path)))

    # Sort by POSIX-style relative path (case-sensitive) rather than by Path
    # objects: Windows paths compare case-insensitively with "\" separators,
    # which would otherwise change the order — and the digest — per OS.
    file_entries.sort(key=lambda entry: entry[0])
    rel_files = [rel for rel, _ in file_entries]

    # Combine all relative paths and hashes in sorted order
    manifest_str = "\n".join(f"{r}:{h}" for r, h in file_entries)
    tree_hash = hashlib.sha256(manifest_str.encode("utf-8")).hexdigest()
    return tree_hash, rel_files


class SkillLockManager:
    """Manages skills.lock creation, verification, and freshness checking."""

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.lock_path = self.workspace_root / "skills.lock"

    def generate_lockfile(self) -> dict:
        """Scan active harness skills and canonical skills and build skills.lock."""
        now = datetime.datetime.now(datetime.timezone.utc).isoformat()
        locked_skills: Dict[str, Any] = {}

        # 1. Active harness skills in .agents/skills
        agents_dir = self.workspace_root / ".agents" / "skills"
        if agents_dir.exists():
            for sdir in sorted(agents_dir.iterdir()):
                if sdir.is_dir() and not sdir.name.startswith("."):
                    sid = sdir.name
                    tree_hash, files = compute_skill_tree_hash(sdir)
                    skill_md = sdir / "SKILL.md"
                    meta: Dict[str, Any] = {}
                    if skill_md.exists():
                        try:
                            from .frontmatter import parse_frontmatter
                            meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                        except Exception:
                            pass
                    locked_skills[sid] = {
                        "version": str(meta.get("version", "1.0.0")),
                        "sha256": tree_hash,
                        "category": str(meta.get("category", "active-harness")),
                        "files": files,
                        "dependencies": meta.get("dependencies", []) or [],
                        "verified_at": meta.get("last_verified", now[:10]),
                        "risk": meta.get("risk", "low")
                    }

        # 2. Canonical skills in skills/
        canonical_dir = self.workspace_root / "skills"
        if canonical_dir.exists():
            for sdir in sorted(canonical_dir.glob("*/*")):
                if sdir.is_dir() and not sdir.name.startswith("_") and (sdir / "SKILL.md").exists():
                    rel = str(sdir.relative_to(canonical_dir)).replace("\\", "/")
                    sid = rel.replace("/", ".")
                    if sid not in locked_skills:
                        tree_hash, files = compute_skill_tree_hash(sdir)
                        meta = {}
                        try:
                            from .frontmatter import parse_frontmatter
                            meta, _ = parse_frontmatter((sdir / "SKILL.md").read_text(encoding="utf-8"))
                        except Exception:
                            pass
                        locked_skills[sid] = {
                            "version": str(meta.get("version", "1.0.0")),
                            "sha256": tree_hash,
                            "category": str(meta.get("category", sdir.parent.name)),
                            "files": files,
                            "dependencies": meta.get("dependencies", []) or [],
                            "verified_at": meta.get("last_verified", now[:10]),
                            "risk": meta.get("risk", "low")
                        }

        lockfile = {
            "version": 1,
            "generated_at": now,
            "generator": "all-skills-lock v1.0.0",
            "total_skills": len(locked_skills),
            "skills": locked_skills
        }
        return lockfile

    def save_lockfile(self) -> Path:
        data = self.generate_lockfile()
        with open(self.lock_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
            f.write("\n")
        return self.lock_path

    def load_lockfile(self) -> Optional[dict]:
        if not self.lock_path.exists():
            return None
        try:
            data = json.loads(self.lock_path.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else None
        except Exception:
            return None

    def verify_skill(self, skill_id: str) -> dict:
        """Cryptographically verify a skill against skills.lock."""
        lock = self.load_lockfile()
        if not lock:
            return {
                "skill": skill_id,
                "status": "error",
                "message": "skills.lock not found. Run 'skills lock' to generate."
            }

        locked_entry = lock.get("skills", {}).get(skill_id)
        if not locked_entry:
            # Check prefix or normalized name
            norm_id = skill_id.replace("active.", "")
            locked_entry = lock.get("skills", {}).get(norm_id)
            if locked_entry:
                skill_id = norm_id

        if not locked_entry:
            return {
                "skill": skill_id,
                "status": "not_locked",
                "message": f"Skill '{skill_id}' is not in skills.lock."
            }

        # Locate skill directory
        skill_dir = None
        candidate_agents = self.workspace_root / ".agents" / "skills" / skill_id
        if candidate_agents.is_dir():
            skill_dir = candidate_agents
        else:
            cand_rel = skill_id.replace(".", "/")
            candidate_canon = self.workspace_root / "skills" / cand_rel
            if candidate_canon.is_dir():
                skill_dir = candidate_canon

        if not skill_dir:
            return {
                "skill": skill_id,
                "status": "missing_directory",
                "message": f"Directory for skill '{skill_id}' could not be located."
            }

        current_hash, current_files = compute_skill_tree_hash(skill_dir)
        expected_hash = locked_entry.get("sha256")

        hash_valid = (current_hash == expected_hash)
        return {
            "skill": skill_id,
            "status": "verified" if hash_valid else "tampered",
            "hash_valid": hash_valid,
            "current_sha256": current_hash,
            "expected_sha256": expected_hash,
            "version": locked_entry.get("version"),
            "files_count": len(current_files),
            "quarantined": False
        }

    def verify_all(self) -> dict:
        """Verify all locked skills in skills.lock."""
        lock = self.load_lockfile()
        if not lock:
            return {"error": "skills.lock not found"}

        results = {}
        passed = 0
        failed = 0
        for sid in lock.get("skills", {}):
            res = self.verify_skill(sid)
            results[sid] = res
            if res.get("status") == "verified":
                passed += 1
            else:
                failed += 1

        return {
            "total": len(results),
            "passed": passed,
            "failed": failed,
            "skills": results
        }

    def check_stale(self, threshold_days: int = 90) -> List[dict]:
        """Detect skills where last_verified exceeds the staleness threshold."""
        today = datetime.date.today()
        stale_skills: List[dict] = []

        # Check active skills in .agents/skills
        agents_dir = self.workspace_root / ".agents" / "skills"
        if agents_dir.exists():
            for sdir in sorted(agents_dir.iterdir()):
                if sdir.is_dir() and (sdir / "SKILL.md").exists():
                    sid = sdir.name
                    try:
                        from .frontmatter import parse_frontmatter
                        meta, _ = parse_frontmatter((sdir / "SKILL.md").read_text(encoding="utf-8"))
                    except Exception:
                        meta = {}

                    verified_str = meta.get("last_verified")
                    days_ago = None
                    if verified_str:
                        try:
                            vdate = datetime.date.fromisoformat(str(verified_str).strip())
                            days_ago = (today - vdate).days
                        except Exception:
                            days_ago = 999
                    else:
                        # Fallback to git/file mtime
                        mtime = (sdir / "SKILL.md").stat().st_mtime
                        fdate = datetime.date.fromtimestamp(mtime)
                        days_ago = (today - fdate).days

                    if days_ago is not None and days_ago > threshold_days:
                        stale_skills.append({
                            "skill": sid,
                            "days_ago": days_ago,
                            "last_verified": verified_str or "unrecorded",
                            "verified_against": meta.get("verified_against", []),
                            "category": meta.get("category", "active")
                        })
        return stale_skills
