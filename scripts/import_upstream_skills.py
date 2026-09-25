#!/usr/bin/env python3
"""Import and deduplicate upstream skills into categorized awesome_skills domains."""
from __future__ import annotations

import argparse
import os
import re
import shutil
from pathlib import Path
from typing import Dict, Set

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"
SRC_SKILLS_DIR = REPO_ROOT / "scratch_import" / "skills"

CATEGORY_MAP = {
    # Finance, Banking & Markets
    "Finance": "finance",
    "Banking": "finance",
    "Crypto & Blockchain": "trading-markets",
    "Accounting": "finance",
    # HR & People
    "HR & People": "hr-people",
    # Healthcare & Life Sciences
    "Healthcare": "healthcare",
    "Biotech": "biotech",
    # Legal & Compliance
    "Legal": "legal",
    # Real Estate & Property
    "Real Estate": "real-estate",
    # Automotive & Mobility
    "Automotive": "automotive",
    "Transportation": "transportation",
    "Aviation": "aerospace",
    # Architecture & Construction
    "Architecture": "architecture",
    "Construction": "construction",
    # Insurance & Risk
    "Insurance": "insurance",
    # Agriculture & Food
    "Agriculture": "agriculture",
    "Food & Beverage": "food-beverage",
    # Energy & Utilities
    "Energy": "energy",
    "Sustainability": "environment-climate",
    # Telecom & Networks
    "Telecom": "telecom",
    # Industry & Manufacturing
    "Manufacturing": "manufacturing",
    # Government & Nonprofit
    "Government": "government",
    "Nonprofit": "nonprofit-ngo",
    # Education & Learning
    "Education": "education",
    "Childcare": "parenting-family",
    # Sales & Marketing
    "Sales & Marketing": "sales",
    "Ecommerce": "ecommerce",
    # Media, Creative & Arts
    "Content Creation": "content-writing",
    "Photography": "photography",
    "Media": "media",
    "Journalism": "media-journalism",
    "Music Industry": "music-audio",
    "Gaming": "game-development",
    "Fashion": "fashion",
    "Beauty & Wellness": "beauty-wellness",
    "Sports & Fitness": "sports",
    "Hospitality": "hospitality",
    "Travel & Tourism": "travel-tourism",
    "Travel": "travel-tourism",
    "Consulting": "consulting",
    "Operations": "operations",
    "Product Management": "product-management",
    "Startup": "business-strategy",
    "Freelance": "career",
    "Personal Development": "personal-development",
    # Tech / Software
    "Development": "development",
    "DevOps": "devops",
    "AI & Automation": "ai-ml",
    "Cybersecurity": "security",
    "Data & Analytics": "data-science",
    "UX Design": "design",
}


def get_existing_skill_ids() -> Set[str]:
    """Collect all skill IDs existing in repository to prevent duplicate overwriting."""
    existing = set()

    # 1. Canonical skills
    canon_dir = REPO_ROOT / "skills"
    if canon_dir.exists():
        for sdir in canon_dir.glob("*/*"):
            if sdir.is_dir() and (sdir / "SKILL.md").exists():
                existing.add(sdir.name.lower())
                existing.add(sdir.parent.name.lower() + "." + sdir.name.lower())

    # 2. Active harness
    agents_dir = REPO_ROOT / ".agents" / "skills"
    if agents_dir.exists():
        for sdir in agents_dir.iterdir():
            if sdir.is_dir():
                existing.add(sdir.name.lower())

    # 3. Awesome skills
    if AWESOME_DIR.exists():
        for cat_dir in AWESOME_DIR.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith("."):
                for sdir in cat_dir.iterdir():
                    if sdir.is_dir():
                        existing.add(sdir.name.lower())

    return existing


def normalize_category(cat_raw: str) -> str:
    cleaned = cat_raw.strip().strip('"\'')
    if cleaned in CATEGORY_MAP:
        return CATEGORY_MAP[cleaned]
    # slugify
    slug = cleaned.lower()
    slug = slug.replace(" & ", "-").replace("&", "-").replace(" ", "-").replace("/", "-")
    slug = re.sub(r"[^a-z0-9-_]", "", slug)
    return slug or "general"


def normalize_skill_frontmatter(md_text: str, skill_name: str, category: str, skill_dir: Path | None = None) -> str:
    """Keep the upstream frontmatter; add category and provenance (never an assumed license).

    Shares the merge and license-detection rules of scripts/sync_sources.py, the
    importer to use for new sources.
    """
    from sync_sources import detect_license, merge_frontmatter, now_utc

    license_id, how = detect_license(skill_dir or SRC_SKILLS_DIR, SRC_SKILLS_DIR.parent, None)
    provenance = {
        "repository": "Winbda/claude-skills-collection",
        "path": f"skills/{skill_name}",
        "license": license_id,
        "license_source": how,
        "imported_at": now_utc(),
    }
    return merge_frontmatter(md_text, skill_name, category, provenance)


def run_import(dry_run: bool = False, max_import: int | None = None) -> dict:
    if not SRC_SKILLS_DIR.exists():
        raise FileNotFoundError(f"Source skills directory not found at {SRC_SKILLS_DIR}")

    existing_ids = get_existing_skill_ids()
    print(f"Loaded {len(existing_ids)} existing skill IDs to prevent duplicates.")

    skills_to_import = [d for d in os.listdir(SRC_SKILLS_DIR) if (SRC_SKILLS_DIR / d).is_dir()]
    print(f"Discovered {len(skills_to_import)} upstream skills in {SRC_SKILLS_DIR}.")

    imported_count = 0
    skipped_duplicates = 0
    category_counts: Dict[str, int] = {}

    for sname in sorted(skills_to_import):
        if max_import and imported_count >= max_import:
            break

        slug_name = sname.lower()
        if slug_name in existing_ids:
            skipped_duplicates += 1
            continue

        skill_src = SRC_SKILLS_DIR / sname
        skill_md = skill_src / "SKILL.md"
        if not skill_md.exists():
            continue

        try:
            txt = skill_md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        cat_raw = "General"
        m_cat = re.search(r"category:\s*([^\n\r]+)", txt[:400])
        if m_cat:
            cat_raw = m_cat.group(1)

        norm_cat = normalize_category(cat_raw)
        dest_dir = AWESOME_DIR / norm_cat / sname

        if not dry_run:
            dest_dir.mkdir(parents=True, exist_ok=True)
            # Copy all files from skill directory
            for f in os.listdir(skill_src):
                src_f = skill_src / f
                dst_f = dest_dir / f
                if src_f.is_file():
                    if f == "SKILL.md":
                        norm_content = normalize_skill_frontmatter(txt, sname, norm_cat, skill_src)
                        dst_f.write_text(norm_content, encoding="utf-8")
                    else:
                        shutil.copy2(str(src_f), str(dst_f))
                elif src_f.is_dir():
                    shutil.copytree(str(src_f), str(dst_f), dirs_exist_ok=True)

        existing_ids.add(slug_name)
        category_counts[norm_cat] = category_counts.get(norm_cat, 0) + 1
        imported_count += 1

    return {
        "imported": imported_count,
        "skipped_duplicates": skipped_duplicates,
        "categories": category_counts
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Import upstream skills into awesome_skills")
    parser.add_argument("--dry-run", action="store_true", help="Simulate import without copying files")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of skills imported")
    args = parser.parse_args()

    results = run_import(dry_run=args.dry_run, max_import=args.limit)

    print("\n" + "=" * 50)
    print("           UPSTREAM IMPORT SUMMARY")
    print("=" * 50)
    print(f"Mode:               {'DRY RUN' if args.dry_run else 'LIVE IMPORT'}")
    print(f"New Skills Added:   {results['imported']}")
    print(f"Duplicates Skipped: {results['skipped_duplicates']}")
    print(f"Categories Updated: {len(results['categories'])}")
    print("-" * 50)
    print("Top Categories Populated:")
    for cat, cnt in sorted(results["categories"].items(), key=lambda x: -x[1])[:30]:
        print(f"  {cat:<25}: +{cnt} skills")
    print("=" * 50)


if __name__ == "__main__":
    main()
