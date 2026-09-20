#!/usr/bin/env python3
"""Sequentially shallow-clone priority upstream repositories, extract and normalize skills into awesome_skills, and clean up transient clones."""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"
SCRATCH_DIR = REPO_ROOT / "scratch_priority_import"

# 20 Priority Repositories with their primary target domains
PRIORITY_REPOS = [
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

SLUG_CLEANER = re.compile(r"[^a-z0-9-_]")


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[\s_]+", "-", s)
    s = SLUG_CLEANER.sub("", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s or "unnamed-skill"


def get_existing_skill_slugs() -> Set[str]:
    slugs = set()
    # Canonical
    canon_dir = REPO_ROOT / "skills"
    if canon_dir.exists():
        for sdir in canon_dir.glob("*/*"):
            if sdir.is_dir() and (sdir / "SKILL.md").exists():
                slugs.add(sdir.name.lower())
    # Harness
    harness_dir = REPO_ROOT / ".agents" / "skills"
    if harness_dir.exists():
        for sdir in harness_dir.iterdir():
            if sdir.is_dir():
                slugs.add(sdir.name.lower())
    # Awesome
    if AWESOME_DIR.exists():
        for cat_dir in AWESOME_DIR.iterdir():
            if cat_dir.is_dir() and not cat_dir.name.startswith("."):
                for sdir in cat_dir.iterdir():
                    if sdir.is_dir():
                        slugs.add(sdir.name.lower())
    return slugs


def normalize_frontmatter(raw_text: str, skill_slug: str, cat: str, repo_info: dict, rel_path: str) -> str:
    desc = f"Expert instructions and domain workflows for {skill_slug.replace('-', ' ')}."
    body = raw_text
    risk = "low"

    if raw_text.startswith("---"):
        parts = raw_text.split("---", 2)
        if len(parts) >= 3:
            fm_text = parts[1]
            body = parts[2]
            m_desc = re.search(r"description:\s*\|?\s*([^\n\r]+(?:\n\s+[^\n\r]+)*)", fm_text)
            if m_desc:
                clean_d = " ".join(line.strip() for line in m_desc.group(1).splitlines() if line.strip())
                if len(clean_d) >= 10:
                    desc = clean_d.replace('"', "'")
            m_risk = re.search(r"risk:\s*([^\n\r]+)", fm_text)
            if m_risk:
                r_val = m_risk.group(1).strip().strip('"\'').lower()
                if r_val in {"low", "medium", "high", "critical"}:
                    risk = r_val

    # Strip newlines from description and cap
    desc = desc[:300].replace("\n", " ").strip()
    clean_fm = f"""---
name: {skill_slug}
description: "{desc}"
category: {cat}
version: 1.0.0
disable-model-invocation: false
risk: {risk}
source: "https://github.com/{repo_info['repo']}"
source_repository: "{repo_info['repo']}"
source_path: "{rel_path}"
license: "{repo_info['license']}"
imported_at: "2026-09-20"
---
"""
    return clean_fm + body.lstrip()


def clone_repo(repo: str, target_dir: Path) -> bool:
    url = f"https://github.com/{repo}.git"
    if target_dir.exists():
        shutil.rmtree(target_dir, ignore_errors=True)
    cmd = ["git", "clone", "--depth", "1", url, str(target_dir)]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, timeout=60)
        return res.returncode == 0
    except Exception as e:
        print(f"Clone error for {repo}: {e}")
        return False


def discover_skills_in_repo(repo_dir: Path) -> List[Tuple[Path, str]]:
    """Find skill directories or markdown playbooks in cloned repository."""
    discovered: List[Tuple[Path, str]] = []
    
    # Check standard SKILL.md locations
    for skill_md in repo_dir.rglob("SKILL.md"):
        if ".git" in skill_md.parts:
            continue
        discovered.append((skill_md.parent, skill_md.parent.name))

    # Also check if repository has skill-like directories (e.g. scientific-agents expert profiles)
    if not discovered:
        for md_file in repo_dir.rglob("*.md"):
            if ".git" in md_file.parts or md_file.name.lower() in {"readme.md", "license.md", "contributing.md", "code_of_conduct.md"}:
                continue
            if md_file.name.lower() in {"agents.md", "instructions.md"} or "skills" in md_file.parts:
                parent_name = md_file.parent.name
                if parent_name and parent_name != repo_dir.name:
                    discovered.append((md_file.parent, parent_name))

    seen_dirs = set()
    unique_discovered = []
    for sdir, sname in discovered:
        if sdir not in seen_dirs:
            seen_dirs.add(sdir)
            unique_discovered.append((sdir, sname))
    return unique_discovered


def import_repository(repo_info: dict, existing_slugs: Set[str]) -> dict:
    repo_name = repo_info["repo"]
    default_cat = repo_info["default_cat"]
    clone_target = SCRATCH_DIR / repo_name.replace("/", "_")
    
    print(f"\nProcessing upstream repo: {repo_name} -> {default_cat}...")
    success = clone_repo(repo_name, clone_target)
    if not success:
        print(f"  Warning: Could not clone {repo_name}. Will note status and rely on synthesis fallback.")
        return {"repo": repo_name, "status": "clone_failed", "imported": 0}

    skill_entries = discover_skills_in_repo(clone_target)
    print(f"  Discovered {len(skill_entries)} skill candidates in {repo_name}.")

    imported_count = 0
    skipped_count = 0

    for sdir, raw_name in skill_entries:
        skill_slug = slugify(raw_name)
        if not skill_slug or len(skill_slug) < 3:
            skill_slug = slugify(sdir.name)
        if skill_slug in existing_slugs:
            skipped_count += 1
            continue

        inst_file = sdir / "SKILL.md"
        if not inst_file.exists():
            for candidate in ["AGENTS.md", "instructions.md", f"{raw_name}.md"]:
                if (sdir / candidate).exists():
                    inst_file = sdir / candidate
                    break
        if not inst_file or not inst_file.exists():
            continue

        try:
            content = inst_file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        cat = default_cat
        m_cat = re.search(r"category:\s*([a-z0-9-_]+)", content[:400], re.IGNORECASE)
        if m_cat:
            cat_found = slugify(m_cat.group(1))
            if cat_found and cat_found not in {"general", "skill"}:
                cat = cat_found

        target_dir = AWESOME_DIR / cat / skill_slug
        target_dir.mkdir(parents=True, exist_ok=True)

        rel_path = str(inst_file.relative_to(clone_target)).replace("\\", "/")
        norm_text = normalize_frontmatter(content, skill_slug, cat, repo_info, rel_path)
        (target_dir / "SKILL.md").write_text(norm_text, encoding="utf-8")

        for child in sdir.iterdir():
            if child == inst_file or child.name.startswith(".") or child.name == ".git":
                continue
            dst_child = target_dir / child.name
            try:
                if child.is_file():
                    shutil.copy2(str(child), str(dst_child))
                elif child.is_dir():
                    shutil.copytree(str(child), str(dst_child), dirs_exist_ok=True)
            except Exception:
                pass

        existing_slugs.add(skill_slug)
        imported_count += 1

    shutil.rmtree(clone_target, ignore_errors=True)
    print(f"  Finished {repo_name}: imported {imported_count}, skipped {skipped_count}. Scratch cleaned.")

    return {
        "repo": repo_name,
        "status": "success",
        "imported": imported_count,
        "skipped": skipped_count
    }


def main():
    print("=" * 60)
    print("      PRIORITY UPSTREAM SKILLS INGESTION ENGINE")
    print("=" * 60)
    SCRATCH_DIR.mkdir(parents=True, exist_ok=True)

    existing_slugs = get_existing_skill_slugs()
    print(f"Initial existing skill slugs: {len(existing_slugs):,}")

    results = []
    for repo_info in PRIORITY_REPOS:
        res = import_repository(repo_info, existing_slugs)
        results.append(res)

    if SCRATCH_DIR.exists():
        shutil.rmtree(SCRATCH_DIR, ignore_errors=True)

    total_imported = sum(r.get("imported", 0) for r in results)
    print("\n" + "=" * 60)
    print("                 INGESTION SUMMARY")
    print("=" * 60)
    print(f"Total Repositories Processed: {len(results)}")
    print(f"Total New Skills Ingested:    {total_imported}")
    print(f"Total Unique Skill Slugs:     {len(existing_slugs):,}")
    print("=" * 60)


if __name__ == "__main__":
    main()
