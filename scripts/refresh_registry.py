"""Refresh registry.json with metadata backfilled from each SKILL.md.

Reads the existing registry, merges per-skill frontmatter fields that are not
yet present in the JSON (lifecycle, capabilities, inputs, outputs, permissions,
compatibility), recomputes deterministic quality scores, and writes both
registry.json and dependencies.json.

Usage:
    python scripts/refresh_registry.py             # write both files
    python scripts/refresh_registry.py --check     # exit 1 if either file is stale
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skills.registry import load_registry  # noqa: E402
from skills.frontmatter import parse_frontmatter  # noqa: E402
from skills.quality import score_all  # noqa: E402
from skills.dependencies import generate_dependencies_json  # noqa: E402

# Frontmatter fields that should flow from SKILL.md into the registry entry.
MERGE_FIELDS = (
    "lifecycle",
    "capabilities",
    "inputs",
    "outputs",
    "permissions",
    "compatibility",
)


def _merge_frontmatter(registry, skills_root: Path) -> int:
    changed = 0
    for entry in registry.entries:
        skill_md = skills_root / Path(*entry.path.split("/")) / "SKILL.md"
        if not skill_md.exists():
            continue
        try:
            meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except Exception:
            continue
        for field in MERGE_FIELDS:
            if field not in meta:
                continue
            value = meta[field]
            if value in (None, "", []):
                continue
            if getattr(entry, field) != value:
                setattr(entry, field, value)
                changed += 1
    return changed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Verify registry.json + dependencies.json are current without writing.",
    )
    args = parser.parse_args()

    registry = load_registry(ROOT)
    skills_root = ROOT / "skills"
    merged = _merge_frontmatter(registry, skills_root)

    reports = score_all(registry, skills_root)
    for entry in registry.entries:
        report = reports[entry.id]
        entry.quality = report.to_dict()
        entry.quality_score = report.overall_score

    registry_path = skills_root / "registry.json"
    deps_path = skills_root / "dependencies.json"

    new_registry = registry.to_json() + "\n"
    current_registry = registry_path.read_text(encoding="utf-8") if registry_path.exists() else ""

    deps_data = generate_dependencies_json(registry.entries)
    new_deps = json.dumps(deps_data, indent=2) + "\n"
    current_deps = deps_path.read_text(encoding="utf-8") if deps_path.exists() else ""

    if args.check:
        stale = []
        if new_registry != current_registry:
            stale.append("registry.json is out of date (run python scripts/refresh_registry.py)")
        if new_deps != current_deps:
            stale.append("dependencies.json is out of date (run python scripts/refresh_registry.py)")
        for message in stale:
            print(f"STALE: {message}")
        if stale:
            return 1
        print(f"registry.json and dependencies.json are current ({len(registry.entries)} skills).")
        return 0

    registry_path.write_text(new_registry, encoding="utf-8")
    deps_path.write_text(new_deps, encoding="utf-8")
    print(f"Refreshed {len(registry.entries)} skills ({merged} metadata fields merged).")
    print(f"Wrote {registry_path}")
    print(f"Wrote {deps_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())