#!/usr/bin/env python3
"""Import the priority upstream skill repositories through the shared sync pipeline.

This script used to be a separate importer that rewrote every ``SKILL.md``
(dropping most frontmatter, resetting ``version`` and forcing
``disable-model-invocation: false``), stamped a hard-coded date and licence,
recorded no commit — and, when it finished, deleted ``scratch_priority_import/``,
which is a shipped Python package, not a scratch folder.

It now delegates to :mod:`sync_sources`, so priority imports get the same
guarantees as every other import: complete packages, preserved upstream
metadata, licences detected from the repository (``NOASSERTION`` when unknown —
the ``license`` below is only a declared fallback), full commit SHAs, real
timestamps, and reviewed updates with backups and rollback. Clones live in the
git-ignored ``scratch/`` directory.

Usage:
    python scripts/import_priority_repos.py                    # import new skills
    python scripts/import_priority_repos.py --update           # review upstream changes (no writes)
    python scripts/import_priority_repos.py --update --apply   # apply reviewed updates (with backup)
    python scripts/import_priority_repos.py --repo K-Dense-AI/scientific-agent-skills
    python scripts/import_priority_repos.py --list
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, str(Path(__file__).resolve().parent))
import sync_sources  # noqa: E402

# Priority repositories and the catalog category their new skills are placed in.
# ``license`` is a declared fallback used only when the repository has no
# recognisable LICENSE file.
PRIORITY_REPOS: List[Dict[str, str]] = [
    {
        "repo": "K-Dense-AI/scientific-agent-skills",
        "default_cat": "science-research",
        "domain": "Scientific Computing & Lab Automation",
        "license": "MIT",
    },
    {
        "repo": "K-Dense-AI/scientific-agents",
        "default_cat": "engineering",
        "domain": "Scientist & Engineer Practitioner Profiles",
        "license": "MIT",
    },
    {
        "repo": "VLSIDA/vlsida-skills",
        "default_cat": "semiconductor",
        "domain": "Semiconductor EDA & Physical Design",
        "license": "Apache-2.0",
    },
    {
        "repo": "Power-Agent/PowerSkills",
        "default_cat": "electrical-engineering",
        "domain": "Electrical Power Systems & Grid Analysis",
        "license": "MIT",
    },
    {
        "repo": "rahulbachina/robotics-skills",
        "default_cat": "robotics",
        "domain": "Robotics, SLAM & ROS2 Navigation",
        "license": "MIT",
    },
    {
        "repo": "danmaps/gis-agent-skills",
        "default_cat": "geospatial",
        "domain": "GIS & Spatial Geospatial Analysis",
        "license": "MIT",
    },
    {
        "repo": "panpanc/math-skills",
        "default_cat": "mathematics",
        "domain": "Mathematics & Conceptual Proofs",
        "license": "MIT",
    },
    {
        "repo": "AccessLint/skills",
        "default_cat": "accessibility",
        "domain": "WCAG 2.2 Accessibility Auditing",
        "license": "MIT",
    },
    {
        "repo": "mtnrabi/travel-agent-skills",
        "default_cat": "travel-tourism",
        "domain": "Travel & Fare Optimization",
        "license": "MIT",
    },
    {
        "repo": "machina-sports/sports-skills",
        "default_cat": "sports",
        "domain": "Sports Analytics & Live Data",
        "license": "MIT",
    },
    {
        "repo": "jskherman/engg-skills",
        "default_cat": "chemical-engineering",
        "domain": "Chemical & Process Engineering",
        "license": "MIT",
    },
    {
        "repo": "claudius-ars/embedded-agent-skills",
        "default_cat": "embedded",
        "domain": "Embedded Systems & Hardware GPIO",
        "license": "MIT",
    },
    {
        "repo": "hectorperezvicente/aerospace-skills",
        "default_cat": "aerospace",
        "domain": "Aerospace & Rocketry Telemetry",
        "license": "MIT",
    },
    {
        "repo": "tizzy916/humanities-writing-companion",
        "default_cat": "humanities",
        "domain": "Humanities, History & Classics",
        "license": "MIT",
    },
    {
        "repo": "JonasWeinert/EconAgentSkills",
        "default_cat": "economics",
        "domain": "Economics & Econometrics Research",
        "license": "MIT",
    },
    {
        "repo": "gasquet82-code/procurement-agent-skills",
        "default_cat": "procurement",
        "domain": "Procurement & Strategic Sourcing",
        "license": "MIT",
    },
    {
        "repo": "Shopify/agent-skills",
        "default_cat": "ecommerce",
        "domain": "Shopify Platform & Commerce Storefronts",
        "license": "MIT",
    },
    {
        "repo": "woocommerce/agent-skills",
        "default_cat": "ecommerce",
        "domain": "WooCommerce & Extension Development",
        "license": "GPL-3.0",
    },
    {
        "repo": "srini047/skills-i8n",
        "default_cat": "languages",
        "domain": "Internationalization & Multilingual Skills",
        "license": "MIT",
    },
    {
        "repo": "chunpu/agent-skills",
        "default_cat": "film-tv",
        "domain": "Media Production & Video Storyboarding",
        "license": "MIT",
    },
]


def as_sources(repos: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Convert priority entries into ``sync_sources`` source definitions."""
    return [
        {
            "id": r["repo"].lower().replace("/", "-"),
            "repo": r["repo"],
            "category": r["default_cat"],
            "license": r.get("license"),
        }
        for r in repos
    ]


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Import the priority upstream skill repositories")
    parser.add_argument("--repo", action="append", help="Only this repository (owner/name, repeatable)")
    parser.add_argument("--update", action="store_true", help="Review updates to existing imports (no writes)")
    parser.add_argument("--apply", action="store_true", help="With --update: apply the reviewed updates")
    parser.add_argument("--list", action="store_true", help="List the priority repositories and exit")
    args = parser.parse_args(argv)

    repos = PRIORITY_REPOS
    if args.repo:
        wanted = {r.lower() for r in args.repo}
        repos = [r for r in PRIORITY_REPOS if r["repo"].lower() in wanted]
        unknown = wanted - {r["repo"].lower() for r in repos}
        if unknown:
            print(f"Unknown priority repositories: {', '.join(sorted(unknown))}", file=sys.stderr)
            return 1
    if args.list:
        for r in repos:
            print(f"{r['repo']:45} -> {r['default_cat']:22} {r['domain']}")
        return 0
    if args.apply and not args.update:
        print("--apply requires --update", file=sys.stderr)
        return 2
    return sync_sources.run(as_sources(repos), args.update, args.apply)


if __name__ == "__main__":
    sys.exit(main())
