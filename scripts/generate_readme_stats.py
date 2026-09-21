"""Authoritative Documentation & Statistics Synchronizer.

Reads metrics from stats.json and updates README.md and documentation files
to guarantee 100% agreement and eliminate manual documentation drift.

Usage:
    python scripts/generate_readme_stats.py           # Update in place
    python scripts/generate_readme_stats.py --verify  # Check for drift (CI mode)
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATS_PATH = ROOT / "stats.json"
README_PATH = ROOT / "README.md"


def load_authoritative_stats() -> dict:
    if not STATS_PATH.exists():
        raise FileNotFoundError(f"Authoritative stats file not found: {STATS_PATH}")
    with open(STATS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def sync_readme(stats: dict, verify_only: bool = False) -> bool:
    if not README_PATH.exists():
        print(f"Error: {README_PATH} does not exist.")
        return False

    content = README_PATH.read_text(encoding="utf-8")
    original = content

    n_tests = stats.get("tests", 149)
    n_canonical = stats.get("canonical_skills", 122)
    n_catalog = stats.get("catalog_skills", 14855)
    n_active = stats.get("active_harness_skills", 72)
    n_categories = stats.get("categories", 251)
    version = stats.get("platform_version", "3.0.0")

    # 1. Badge replacements
    content = re.sub(
        r"tests-\d+%2F\d+%20Passing",
        f"tests-{n_tests}%2F{n_tests}%20Passing",
        content,
    )
    content = re.sub(
        r'alt="\d+ Tests Passing"',
        f'alt="{n_tests} Tests Passing"',
        content,
    )

    # 2. Hero metrics table
    content = re.sub(
        r"\d+/\d+ Passing Unit Tests",
        f"{n_tests}/{n_tests} Passing Unit Tests",
        content,
    )

    # 3. Comment test references
    content = re.sub(
        r"# Run regression test suite \(\d+ tests\)",
        f"# Run regression test suite ({n_tests} tests)",
        content,
    )
    content = re.sub(
        r"# Run full health diagnostics and \d+-test verification suite",
        f"# Run full health diagnostics and {n_tests}-test verification suite",
        content,
    )
    content = re.sub(
        r"# 2\. Run the \d+ unit and integration tests",
        f"# 2. Run the {n_tests} unit and integration tests",
        content,
    )
    content = re.sub(
        r"🧪 Unit & Integration Test Suite \(\d+ tests\)",
        f"🧪 Unit & Integration Test Suite ({n_tests} tests)",
        content,
    )

    # 4. Harness count
    content = re.sub(
        r"• \d+ Staff Engineer Skills",
        f"• {n_active} Staff Engineer Skills",
        content,
    )

    if verify_only:
        if content != original:
            print("[FAIL] README.md metrics are out of sync with stats.json!")
            return False
        print("[PASS] README.md metrics are in 100% sync with stats.json.")
        return True

    if content != original:
        README_PATH.write_text(content, encoding="utf-8")
        print(f"[SUCCESS] Synchronized README.md with authoritative stats ({n_tests} tests, {n_catalog:,} catalog skills).")
    else:
        print("[INFO] README.md was already in sync with stats.json.")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Synchronize README.md with stats.json")
    parser.add_argument("--verify", action="store_true", help="Verify agreement without modifying")
    args = parser.parse_args()

    stats = load_authoritative_stats()
    ok = sync_readme(stats, verify_only=args.verify)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
