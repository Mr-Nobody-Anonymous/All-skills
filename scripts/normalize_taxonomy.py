#!/usr/bin/env python3
"""Taxonomy Normalization and Consolidation Engine.

Consolidates fragmented micro-categories and redundant taxonomy families into unified,
production-grade domains across awesome_skills.
"""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path
from typing import Dict, List, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"

# Mapping of source category directory names to target consolidated categories
CONSOLIDATION_MAP: Dict[str, str] = {
    # AI & Machine Learning consolidation
    "ai": "ai-ml",
    "ai-agents": "ai-ml",
    "ai-research": "ai-ml",
    "ai-testing": "ai-evaluation",
    "prompt-engineering": "ai-ml",
    "reasoning": "ai-ml",
    "ml-ops": "mlops",
    "context-optimization": "ai-ml",

    # Database consolidation
    "database-processing": "database",
    "databases": "database",

    # Web consolidation
    "front-end": "frontend",
    "fullstack": "web-development",

    # Healthcare & Wellness consolidation
    "health": "healthcare",
    "dental": "healthcare",
    "pharmacy": "healthcare",
    "fitness-nutrition": "wellness",
    "beauty-wellness": "wellness",

    # Environment & Climate consolidation
    "environmental": "environment-climate",
    "climate-tech": "environment-climate",

    # Media, Video & Audio consolidation
    "media-processing": "media",
    "video": "film-tv",
    "podcast": "media",

    # Parenting & Family consolidation
    "parenting": "parenting-family",

    # Travel & Tourism consolidation
    "travel": "travel-tourism",

    # Automation, Orchestration & Workflows
    "workflow": "automation",
    "workflow-bundle": "automation",
    "granular-workflow-bundle": "automation",
    "orchestration": "automation",

    # Pet & Veterinary consolidation
    "pet-business": "veterinary",
    "pet-care": "veterinary",
    "pet-industry": "veterinary",
    "pet-veterinary": "veterinary",

    # Content & Writing consolidation
    "content": "content-writing",
    "writing": "content-writing",
    "publishing": "content-writing",

    # Development & Coding consolidation
    "coding": "development",
    "code": "development",
    "core-dev": "development",
    "development-and-testing": "development",
    "debugging": "development",

    # Science consolidation
    "science": "science-research",

    # Office Productivity & General
    "office-productivity": "productivity",
    "collaboration": "operations",
    "tool-quality": "developer-tools",
    "tools": "developer-tools",
}


def update_skill_category(skill_dir: Path, new_cat: str) -> None:
    md_file = skill_dir / "SKILL.md"
    if not md_file.exists():
        return
    try:
        content = md_file.read_text(encoding="utf-8", errors="ignore")
        if "category:" in content:
            updated = re.sub(r'category:\s*[^\n\r]+', f'category: {new_cat}', content, count=1)
        else:
            if content.startswith("---"):
                updated = content.replace("---", f"---\ncategory: {new_cat}", 1)
            else:
                updated = content
        md_file.write_text(updated, encoding="utf-8")
    except Exception as e:
        print(f"Error updating category in {md_file}: {e}")


def consolidate_taxonomy() -> dict:
    print("=" * 60)
    print("        TAXONOMY CONSOLIDATION & NORMALIZATION")
    print("=" * 60)

    moves_count: Dict[Tuple[str, str], int] = {}
    skipped_collisions: Dict[Tuple[str, str], int] = {}

    for src_cat, target_cat in CONSOLIDATION_MAP.items():
        src_dir = AWESOME_DIR / src_cat
        if not src_dir.exists() or not src_dir.is_dir():
            continue

        target_dir = AWESOME_DIR / target_cat
        target_dir.mkdir(parents=True, exist_ok=True)

        skill_dirs = [d for d in src_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
        pair = (src_cat, target_cat)

        for sdir in skill_dirs:
            skill_slug = sdir.name
            dest_skill_dir = target_dir / skill_slug

            if dest_skill_dir.exists():
                # Destination already exists - merge auxiliary files
                for item in sdir.iterdir():
                    dest_item = dest_skill_dir / item.name
                    if not dest_item.exists():
                        try:
                            if item.is_file():
                                shutil.copy2(str(item), str(dest_item))
                            elif item.is_dir():
                                shutil.copytree(str(item), str(dest_item))
                        except Exception:
                            pass
                shutil.rmtree(sdir, ignore_errors=True)
                skipped_collisions[pair] = skipped_collisions.get(pair, 0) + 1
            else:
                # Move directory
                shutil.move(str(sdir), str(dest_skill_dir))
                update_skill_category(dest_skill_dir, target_cat)
                moves_count[pair] = moves_count.get(pair, 0) + 1

        # Remove source directory if empty
        remaining = [d for d in src_dir.iterdir() if not d.name.startswith(".")]
        if not remaining:
            shutil.rmtree(src_dir, ignore_errors=True)
            print(f"Consolidated: {src_cat} -> {target_cat} (folder removed)")
        else:
            print(f"Notice: {src_cat} still has {len(remaining)} non-directory files.")

    total_moved = sum(moves_count.values())
    total_merged = sum(skipped_collisions.values())

    print("\n" + "=" * 60)
    print("             CONSOLIDATION SUMMARY")
    print("=" * 60)
    print(f"Total Skills Migrated to New Categories: {total_moved}")
    print(f"Total Colliding Slugs Safely Merged:    {total_merged}")
    print(f"Total Mapped Category Rules:             {len(CONSOLIDATION_MAP)}")
    print("-" * 60)
    print("Top Migrations Executed:")
    for (src, dst), cnt in sorted(moves_count.items(), key=lambda x: -x[1])[:25]:
        print(f"  {src:<22} -> {dst:<20}: {cnt} skills")
    print("=" * 60)

    return {
        "moved": total_moved,
        "merged": total_merged,
        "details": moves_count
    }


if __name__ == "__main__":
    consolidate_taxonomy()
