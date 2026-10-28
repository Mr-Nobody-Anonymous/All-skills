#!/usr/bin/env python3
"""Add the domain skills that the library was missing.

Covers the authoring domains that had no coverage at all before: geospatial/GIS,
CAD and BIM, 3D/Blender/VFX, audio, video, photography and architecture.

    python scripts/dev/add_domain_skills.py            # add missing only
    python scripts/dev/add_domain_skills.py --force    # rewrite existing

Afterwards regenerate the derived artifacts:

    python scripts/refresh_registry.py
    python scripts/compute_stats.py && python scripts/generate_readme_stats.py
    python scripts/generate_baselines.py && python scripts/skills/skills.py lock
    python scripts/sync_federated_registry.py
    node scripts/dev/generate-skill-triggers.js --refresh-digests
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import add_missing_skills as base  # noqa: E402
import domain_skills_geo as geo  # noqa: E402
import domain_skills_media as media  # noqa: E402

FORCE = "--force" in sys.argv
TITLES = {**geo.TITLES, **media.TITLES}
SWITCHED: list[str] = []


def main() -> int:
    # render() looks names up in the base module's title map; merge ours in.
    for name, title in TITLES.items():
        if name not in base.TITLE_OVERRIDES:
            base.TITLE_OVERRIDES[name] = title
        elif base.TITLE_OVERRIDES[name] != title:
            base.TITLE_OVERRIDES[name] = title
            SWITCHED.append(name)

    existing = {path.parent.name for path in base.SKILLS.rglob("SKILL.md")}
    written, skipped = [], []
    for data in [*geo.SKILLS, *media.SKILLS]:
        if data["name"] in existing and not FORCE:
            skipped.append(data["name"])
            continue
        target = base.SKILLS / data["category"] / data["name"]
        target.mkdir(parents=True, exist_ok=True)
        (target / "SKILL.md").write_text(base.render(data), encoding="utf-8")
        title = TITLES.get(data["name"], data["name"].replace("-", " ").title())
        pairs = ", ".join(f"`{p}`" for p in data["pairs"]) or "—"
        (target / "README.md").write_text(
            f"# {title}\n\n{data['description']}\n\n"
            f"- **Skill ID:** {data['category']}.{data['name']}\n"
            f"- **Instructions:** [SKILL.md](SKILL.md)\n"
            f"- **Related:** {pairs}\n"
            f"- **Source:** See ../../registry/provenance.json for provenance and license details.\n",
            encoding="utf-8",
        )
        written.append(f"{data['category']}/{data['name']}")

    print(f"wrote {len(written)} skill(s)")
    for item in written:
        print(f"  skills/{item}/SKILL.md")
    if skipped:
        print(f"skipped {len(skipped)} already present: {', '.join(skipped)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
