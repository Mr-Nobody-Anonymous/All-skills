#!/usr/bin/env python3
"""Generate or verify ``awesome_skills.lock`` — the catalog integrity snapshot.

Every catalog entry (``awesome_skills/<category>/<skill>/SKILL.md``) is pinned by
the SHA-256 of its ``SKILL.md`` with LF-normalised line endings, so the digest is
identical on Windows (``core.autocrlf``) and POSIX checkouts. Metadata (category,
version, license, risk) is copied from ``awesome_skills/skills_index.json``.

Usage:
    python scripts/build_awesome_lock.py            # rewrite awesome_skills.lock
    python scripts/build_awesome_lock.py --verify    # fail if the lock has drifted
    python scripts/build_awesome_lock.py --json      # machine-readable summary
"""

from __future__ import annotations

import argparse
import datetime
import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
LOCK_PATH = REPO_ROOT / "awesome_skills.lock"
INDEX_PATH = REPO_ROOT / "awesome_skills" / "skills_index.json"
CATALOG_DIR = REPO_ROOT / "awesome_skills"
FORMAT = "AAS-Awesome-Lock-v2"


def _sha256(path: Path) -> str:
    import hashlib

    data = path.read_bytes()
    if b"\0" not in data:
        data = data.replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def load_index() -> dict[str, dict]:
    if not INDEX_PATH.exists():
        return {}
    with open(INDEX_PATH, encoding="utf-8") as f:
        entries = json.load(f)
    return {entry["path"]: entry for entry in entries if entry.get("path")}


def build_lock() -> dict:
    index = load_index()
    records: dict[str, dict] = {}
    for skill_md in sorted(CATALOG_DIR.glob("*/*/SKILL.md")):
        rel = skill_md.relative_to(REPO_ROOT).as_posix()
        key = rel[len("awesome_skills/"):-len("/SKILL.md")]
        meta = index.get(rel, {})
        records[key] = {
            "skill_id": meta.get("id") or skill_md.parent.name,
            "category": meta.get("category") or skill_md.parent.parent.name,
            "version": meta.get("version") or "1.0.0",
            "sha256": _sha256(skill_md),
            "source_repo": meta.get("source") or "unknown",
            "license": meta.get("license") or "unknown",
            "risk": meta.get("risk") or "unknown",
            "last_verified": datetime.date.today().isoformat(),
        }
    return {
        "version": "2.0.0",
        "format": FORMAT,
        "generated_at": datetime.date.today().isoformat(),
        "digest": "sha256 of SKILL.md, LF-normalised (CRLF and CR are treated as LF)",
        "total_skills": len(records),
        "skills": records,
    }


def verify() -> tuple[bool, list[str]]:
    if not LOCK_PATH.exists():
        return False, ["awesome_skills.lock is missing"]
    with open(LOCK_PATH, encoding="utf-8") as f:
        lock = json.load(f)
    if lock.get("format") != FORMAT:
        return False, [f"unsupported lock format {lock.get('format')!r}; regenerate with this script"]
    recorded = lock.get("skills", {})
    problems: list[str] = []
    current_keys = set()
    for skill_md in sorted(CATALOG_DIR.glob("*/*/SKILL.md")):
        key = skill_md.relative_to(REPO_ROOT).as_posix()[len("awesome_skills/"):-len("/SKILL.md")]
        current_keys.add(key)
        entry = recorded.get(key)
        if entry is None:
            problems.append(f"missing from lock: {key}")
        elif entry.get("sha256") != _sha256(skill_md):
            problems.append(f"digest mismatch: {key}")
    for key in sorted(set(recorded) - current_keys):
        problems.append(f"no longer in the catalog: {key}")
    return not problems, problems


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate or verify awesome_skills.lock")
    parser.add_argument("--verify", action="store_true", help="Verify without writing")
    parser.add_argument("--json", action="store_true", help="Machine-readable output")
    args = parser.parse_args()

    if args.verify:
        ok, problems = verify()
        if args.json:
            print(json.dumps({"ok": ok, "problems": problems, "checked": len(problems) and None}, default=str))
        elif ok:
            print("Catalog lock verified: every SKILL.md digest matches awesome_skills.lock.")
        else:
            print(f"Catalog lock FAILED with {len(problems)} problem(s):", file=sys.stderr)
            for problem in problems[:20]:
                print(f"  - {problem}", file=sys.stderr)
            if len(problems) > 20:
                print(f"  ... and {len(problems) - 20} more", file=sys.stderr)
        return 0 if ok else 1

    lock = build_lock()
    with open(LOCK_PATH, "w", encoding="utf-8") as f:
        json.dump(lock, f, indent=2)
        f.write("\n")
    if args.json:
        print(json.dumps({"total_skills": lock["total_skills"], "lock": str(LOCK_PATH)}))
    else:
        print(f"Wrote {LOCK_PATH.relative_to(REPO_ROOT)} with {lock['total_skills']:,} catalog entries.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
