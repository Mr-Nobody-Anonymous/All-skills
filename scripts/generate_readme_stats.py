"""Documentation count synchronizer (README.md and every other doc).

A thin CLI over the single rule table in ``scripts/compute_stats.py``
(``DOC_COUNT_RULES``), so there is exactly one definition of which documented
numbers track ``stats.json`` — this script used to keep a second, diverging set
of rules (including ones that re-inserted static "N/N passing" claims).

Usage:
    python scripts/generate_readme_stats.py           # Update in place
    python scripts/generate_readme_stats.py --verify  # Check for drift (CI mode)
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATS_PATH = ROOT / "stats.json"

sys.path.insert(0, str(Path(__file__).resolve().parent))
import compute_stats  # noqa: E402


def load_authoritative_stats() -> dict:
    if not STATS_PATH.exists():
        raise FileNotFoundError(f"Authoritative stats file not found: {STATS_PATH}")
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sync_readme(stats: dict, verify_only: bool = False) -> bool:
    """Sync (or with ``verify_only`` check) every documented count; False on drift."""
    if verify_only:
        problems = compute_stats.verify_docs(stats, ROOT)
        if problems:
            print("[FAIL] Documentation counts are out of sync with stats.json:")
            for problem in problems:
                print(f"  - {problem}")
            return False
        print("[PASS] Documentation counts (README.md, SKILLS.md, CONTRIBUTING.md, docs/) match stats.json.")
        return True

    changed = compute_stats.sync_docs(stats, ROOT)
    if changed:
        print(f"[SUCCESS] Synchronized {', '.join(changed)} with stats.json.")
    else:
        print("[INFO] Documentation counts were already in sync with stats.json.")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize documented counts with stats.json")
    parser.add_argument("--verify", action="store_true", help="Verify agreement without modifying")
    args = parser.parse_args()

    stats = load_authoritative_stats()
    ok = sync_readme(stats, verify_only=args.verify)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
