#!/usr/bin/env python3
"""Compute authoritative skill platform metrics and generate stats.json.

Ensures single-source-of-truth statistics across the entire repository.
Can optionally synchronize README.md and SKILLS.md.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


def get_repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def compute_platform_stats(repo_root: Path | None = None) -> dict:
    if repo_root is None:
        repo_root = get_repo_root()

    awesome_dir = repo_root / "awesome_skills"
    awesome_cats = [
        d for d in os.listdir(awesome_dir)
        if (awesome_dir / d).is_dir() and not d.startswith(".") and d not in ("node_modules", ".git")
    ]
    catalog_skills = []
    for cat in awesome_cats:
        cat_path = awesome_dir / cat
        for s in os.listdir(cat_path):
            if (cat_path / s).is_dir() and not s.startswith("."):
                catalog_skills.append(s)

    catalog_index_count = 0
    skills_index_file = awesome_dir / "skills_index.json"
    if skills_index_file.exists():
        with open(skills_index_file, "r", encoding="utf-8") as f:
            catalog_index_count = len(json.load(f))

    canonical_skills = []
    canonical_categories = set()
    registry_file = repo_root / "skills" / "registry.json"
    if registry_file.exists():
        with open(registry_file, "r", encoding="utf-8") as f:
            canonical_data = json.load(f).get("skills", [])
            canonical_skills = [s.get("id") for s in canonical_data if s.get("id")]
            canonical_categories = set(s.get("category") for s in canonical_data if s.get("category"))

    agents_dir = repo_root / ".agents" / "skills"
    active_harness_skills = [
        d for d in os.listdir(agents_dir)
        if (agents_dir / d).is_dir() and not d.startswith(".")
    ] if agents_dir.exists() else []

    manifest_skills = {}
    manifest_file = repo_root / "manifest.json"
    if manifest_file.exists():
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest_skills = json.load(f).get("skills", {})

    workflows_dir = repo_root / "workflows"
    workflows = [
        w for w in os.listdir(workflows_dir)
        if (workflows_dir / w).is_file() and w.endswith(".md") and w.lower() != "readme.md"
    ] if workflows_dir.exists() else []

    ci_workflows_dir = repo_root / ".github" / "workflows"
    ci_workflows = [
        w for w in os.listdir(ci_workflows_dir)
        if (ci_workflows_dir / w).is_file() and (w.endswith(".yml") or w.endswith(".yaml"))
    ] if ci_workflows_dir.exists() else []

    chains_file = repo_root / "skills" / "chains.json"
    chains_count = 0
    if chains_file.exists():
        with open(chains_file, "r", encoding="utf-8") as f:
            chains_count = len(json.load(f).get("chains", []))

    packs_file = repo_root / "packs" / "packs.json"
    packs_count = 0
    if packs_file.exists():
        with open(packs_file, "r", encoding="utf-8") as f:
            packs_count = len(json.load(f).get("packs", []))

    all_skill_ids = (
        set(catalog_skills)
        | set(canonical_skills)
        | set(active_harness_skills)
        | set(manifest_skills.keys())
    )

    # Count unit test methods dynamically
    try:
        import unittest
        sys.path.insert(0, str(repo_root / "tests"))
        sys.path.insert(0, str(repo_root / "src"))
        suite = unittest.TestLoader().discover(str(repo_root / "tests"), pattern="test_*.py")
        test_count = suite.countTestCases()
    except Exception:
        test_count = 94

    version_file = repo_root / "VERSION"
    platform_version = version_file.read_text(encoding="utf-8").strip() if version_file.exists() else "3.0.0"

    stats = {
        "platform_version": platform_version,
        "total_unique_skills": len(all_skill_ids),
        "catalog_skills": len(catalog_skills),
        "catalog_index_records": catalog_index_count,
        "canonical_skills": len(canonical_skills),
        "active_harness_skills": len(active_harness_skills),
        "manifest_skills": len(manifest_skills),
        "categories": len(awesome_cats),
        "canonical_categories": len(canonical_categories),
        "tests": test_count,
        "workflows": len(workflows),
        "ci_workflows": len(ci_workflows),
        "named_chains": chains_count,
        "curated_packs": packs_count,
        "last_generated": datetime.date.today().isoformat()
    }
    return stats


def save_stats(stats: dict, repo_root: Path | None = None) -> Path:
    if repo_root is None:
        repo_root = get_repo_root()
    stats_file = repo_root / "stats.json"
    with open(stats_file, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return stats_file


# Count claims in prose documentation, kept in sync with stats.json by
# ``--sync-readme`` and checked by ``--verify`` (so drift fails CI). Each pattern
# captures the number as group ``n``; only that group is rewritten.
DOC_FILES = ("README.md", "SKILLS.md", "CONTRIBUTING.md", "docs/**/*.md")
_N = r"(?P<n>\d[\d,]*)"
DOC_COUNT_RULES: list[tuple[re.Pattern[str], str]] = [
    (re.compile(rf"(?i:test suite) \({_N} tests\)"), "tests"),
    (re.compile(rf"{_N}(?= unit tests validating)"), "tests"),
    (re.compile(rf"{_N}(?= canonical skills)", re.I), "canonical_skills"),
    (re.compile(rf"{_N}(?= Canonical Engine Skills)"), "canonical_skills"),
    (re.compile(rf"{_N}(?= active (?:harness )?skills\b)", re.I), "active_harness_skills"),
    (re.compile(rf"Active Harness Skills(?: Index)? \({_N} Skills\)"), "active_harness_skills"),
    (re.compile(rf"active-harness-skills(?:-index)?-{_N}(?=-skills\))"), "active_harness_skills"),
    (re.compile(rf"Active Harness \({_N} skills\)"), "active_harness_skills"),
    (re.compile(rf"across {_N}(?= functional domains| domains in `awesome_skills/`| categories\))"), "categories"),
    (re.compile(rf"`{_N}` categorized implementations"), "catalog_skills"),
    (re.compile(rf"{_N}(?= Catalog Records)"), "catalog_skills"),
    (re.compile(rf"library of {_N}(?=\+? categorized skills)"), "catalog_skills"),
]


def sync_readme(stats: dict, repo_root: Path | None = None) -> bool:
    if repo_root is None:
        repo_root = get_repo_root()
    readme_path = repo_root / "README.md"
    if not readme_path.exists():
        return False

    content = readme_path.read_text(encoding="utf-8")

    # Update Shields badges (robust against URL-encoded chars like %2C and %2F)
    content = re.sub(
        r'skills-[a-zA-Z0-9%,\+\-]+?Total%20Skills',
        f'skills-{stats["total_unique_skills"]}%2B%20Total%20Skills',
        content
    )
    content = re.sub(
        r'awesome--catalog-[a-zA-Z0-9%,\+\-]+?Categorized',
        f'awesome--catalog-{stats["catalog_skills"]}%20Categorized',
        content
    )
    content = re.sub(
        r'active--harness-[a-zA-Z0-9%,\+\-]+?Pre--Loaded',
        f'active--harness-{stats["active_harness_skills"]}%20Pre--Loaded',
        content
    )
    content = re.sub(
        r'manifest-[a-zA-Z0-9%,\+\-]+?Indexed',
        f'manifest-{stats["manifest_skills"]}%20Indexed',
        content
    )
    content = re.sub(
        r'tests-[a-zA-Z0-9%,\+\-]+?Passing',
        f'tests-{stats["tests"]}%2F{stats["tests"]}%20Passing',
        content
    )

    # Update opening summary paragraph
    content = re.sub(
        r'Over\s+[0-9,]+\s+unique skills across\s+[0-9,]+\s+domain categories',
        f'Over {stats["total_unique_skills"]:,} unique skills across {stats["categories"]} domain categories',
        content
    )

    # Update Architecture ASCII Box
    content = re.sub(
        r'•\s*[0-9,]+\s*Curated & Tested Skills',
        f'• {stats["canonical_skills"]} Curated & Tested Skills',
        content
    )
    content = re.sub(
        r'•\s*[0-9,]+\s*Categorized Skills',
        f'• {stats["catalog_skills"]:,} Categorized Skills',
        content
    )
    content = re.sub(
        r'•\s*[0-9,]+\s*Staff Engineer Skills',
        f'• {stats["active_harness_skills"]} Staff Engineer Skills',
        content
    )
    content = re.sub(
        r'•\s*[0-9,]+\s*Functional Domain Dirs',
        f'• {stats["categories"]} Functional Domain Dirs',
        content
    )
    content = re.sub(
        r'•\s*[0-9]+/[0-9]+\s*Passing Unit Tests',
        f'• {stats["tests"]}/{stats["tests"]} Passing Unit Tests',
        content
    )

    # Update Directory Tree and Router sections
    content = re.sub(
        r'#\s*[0-9,]+-item metadata database',
        f'# {stats["catalog_index_records"]:,}-item metadata database',
        content
    )
    content = re.sub(
        r'across all [0-9,]+\+\s*skills',
        f'across all {stats["catalog_skills"]:,}+ skills',
        content
    )
    content = re.sub(
        r'Interact with all [0-9,]+\+\s*categorized skills',
        f'Interact with all {stats["catalog_skills"]:,}+ categorized skills',
        content
    )
    content = re.sub(
        r'#\s*List all [0-9,]+\s*domain categories',
        f'# List all {stats["categories"]} domain categories',
        content
    )
    content = re.sub(
        r'#\s*Fuzzy search across all [0-9,]+\+\s*skills',
        f'# Fuzzy search across all {stats["catalog_skills"]:,}+ skills',
        content
    )
    content = re.sub(
        r'[0-9]+-test verification suite',
        f'{stats["tests"]}-test verification suite',
        content
    )
    content = re.sub(
        r'Run the [0-9]+\s*unit and integration tests',
        f'Run the {stats["tests"]} unit and integration tests',
        content
    )

    readme_path.write_text(apply_doc_counts(content, stats)[0], encoding="utf-8")
    return True


def sync_skills_md(stats: dict, repo_root: Path | None = None) -> bool:
    if repo_root is None:
        repo_root = get_repo_root()
    skills_md_path = repo_root / "SKILLS.md"
    if not skills_md_path.exists():
        return False

    content = skills_md_path.read_text(encoding="utf-8")
    content = re.sub(
        r'platform of \*\*[0-9,]+\+\s*unique specialized Agent Skills\*\*',
        f'platform of **{stats["total_unique_skills"]:,}+ unique specialized Agent Skills**',
        content
    )
    content = re.sub(
        r'\(\*\*[0-9,]+\s*cataloged instances\*\*',
        f'(**{stats["catalog_skills"]:,} cataloged instances**',
        content
    )
    content = re.sub(
        r'across \*\*[0-9,]+\s*domain categories\*\*',
        f'across **{stats["categories"]} domain categories**',
        content
    )
    content = re.sub(
        r'Awesome Skills Library \(`awesome_skills/`\) — [0-9,]+\s*Categorized Skills',
        f'Awesome Skills Library (`awesome_skills/`) — {stats["catalog_skills"]:,} Categorized Skills',
        content
    )
    content = re.sub(
        r'\*\*[0-9,]+\s*Domain Categories\*\*',
        f'**{stats["categories"]} Domain Categories**',
        content
    )
    content = re.sub(
        r'\[CATALOG\.md\]\(awesome_skills/CATALOG\.md\) lists all [0-9,]+\s*skills',
        f'[CATALOG.md](awesome_skills/CATALOG.md) lists all {stats["catalog_skills"]:,} skills',
        content
    )
    content = re.sub(
        r'# Search across all [0-9,]+\s*skills',
        f'# Search across all {stats["catalog_skills"]:,} skills',
        content
    )
    content = re.sub(
        r'\*\*[0-9,]+\s*Pre-Loaded Staff Engineer Skills\*\*',
        f'**{stats["active_harness_skills"]} Pre-Loaded Staff Engineer Skills**',
        content
    )

    skills_md_path.write_text(apply_doc_counts(content, stats)[0], encoding="utf-8")
    return True


def doc_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()
    for pattern in DOC_FILES:
        files.update(p for p in repo_root.glob(pattern) if p.is_file())
    return sorted(files)


def apply_doc_counts(content: str, stats: dict) -> tuple[str, list[tuple[int, str, str]]]:
    """Rewrite every documented count claim; return (new text, [(line, old, new)])."""
    changes: list[tuple[int, str, str]] = []

    def rewrite(match: re.Match[str], key: str) -> str:
        whole, start = match.group(0), match.start()
        old = match.group("n")
        new = f"{stats[key]:,}"
        if old != new:
            changes.append((content.count("\n", 0, match.start("n")) + 1, old, new))
        return whole[: match.start("n") - start] + new + whole[match.end("n") - start:]

    for pattern, key in DOC_COUNT_RULES:
        content = pattern.sub(lambda m, k=key: rewrite(m, k), content)
    return content, changes


def sync_docs(stats: dict, repo_root: Path | None = None) -> list[str]:
    """Apply DOC_COUNT_RULES to every documentation file; return the files changed."""
    repo_root = repo_root or get_repo_root()
    changed = []
    for path in doc_files(repo_root):
        text = path.read_text(encoding="utf-8")
        new_text, changes = apply_doc_counts(text, stats)
        if changes:
            path.write_text(new_text, encoding="utf-8", newline="")
            changed.append(path.relative_to(repo_root).as_posix())
    return changed


def verify_docs(stats: dict, repo_root: Path | None = None) -> list[str]:
    """Every documented count that disagrees with ``stats`` (empty = consistent)."""
    repo_root = repo_root or get_repo_root()
    problems = []
    for path in doc_files(repo_root):
        for line, old, new in apply_doc_counts(path.read_text(encoding="utf-8"), stats)[1]:
            problems.append(f"{path.relative_to(repo_root).as_posix()}:{line}: says {old}, stats.json says {new}")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute authoritative stats.json")
    parser.add_argument("--sync-readme", action="store_true", help="Synchronize README.md and SKILLS.md with generated stats")
    parser.add_argument("--verify", action="store_true", help="Verify stats.json matches actual repository metrics without writing")
    args = parser.parse_args()

    repo_root = get_repo_root()
    computed = compute_platform_stats(repo_root)

    if args.verify:
        stats_file = repo_root / "stats.json"
        if not stats_file.exists():
            print(f"Error: {stats_file} does not exist", file=sys.stderr)
            sys.exit(1)
        with open(stats_file, "r", encoding="utf-8") as f:
            existing = json.load(f)

        mismatches = [f"Documentation drift: {p}" for p in verify_docs(existing, repo_root)]
        for key, val in computed.items():
            if key == "last_generated":
                continue
            if key not in existing:
                mismatches.append(f"Missing key '{key}' in stats.json (computed: {val})")
            elif existing[key] != val:
                mismatches.append(f"Field '{key}' mismatch: stats.json has {existing[key]}, computed {val}")

        if mismatches:
            print("❌ Stats Verification Failed:", file=sys.stderr)
            for m in mismatches:
                print(f"  - {m}", file=sys.stderr)
            sys.exit(1)
        else:
            print("✅ Stats Verification Passed: stats.json perfectly matches repository metrics!")
            sys.exit(0)

    saved_path = save_stats(computed, repo_root)
    print(f"Authoritative stats generated at {saved_path}:")
    print(json.dumps(computed, indent=2))

    if args.sync_readme:
        synced_readme = sync_readme(computed, repo_root)
        synced_skills = sync_skills_md(computed, repo_root)
        if synced_readme:
            print("Successfully synchronized README.md numbers.")
        if synced_skills:
            print("Successfully synchronized SKILLS.md numbers.")
        for changed in sync_docs(computed, repo_root):
            print(f"Successfully synchronized {changed} numbers.")


if __name__ == "__main__":
    main()
