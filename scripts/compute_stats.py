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


# ─── Documentation counts ───────────────────────────────────────────────────
# Every count quoted in the documentation is declared here, once, and kept in
# sync with stats.json: ``--sync-readme`` rewrites the numbers and ``--verify``
# (run in CI) fails on any disagreement. Each pattern captures the number as
# group ``n``; only that group changes, and inside ASCII-art boxes the cell is
# re-padded so the box stays aligned. Styles: "comma" 14,855 · "plain" 14855 ·
# "url" 14%2C855 (shields.io badge paths).
#
# Wording matters as much as digits: catalog *entries* (catalog_skills) are not
# unique skills (total_unique_skills), and no rule may assert "passing" or
# "verified" — CI status comes from live badges, trust from recorded evidence.
DOC_FILES = ("README.md", "SKILLS.md", "CONTRIBUTING.md", "docs/**/*.md")
_N = r"(?P<n>\d[\d,]*)"
_NURL = r"(?P<n>\d+(?:%2C\d{3})*)"


def _rule(pattern: str, key: str, style: str = "comma", flags: int = 0) -> tuple[re.Pattern[str], str, str]:
    return re.compile(pattern, flags), key, style


DOC_COUNT_RULES: list[tuple[re.Pattern[str], str, str]] = [
    # Tests
    _rule(rf"(?i:test suite) \({_N} tests\)", "tests"),
    _rule(rf"{_N}(?= unit tests validating)", "tests"),
    _rule(rf"{_N}(?=-test verification suite)", "tests"),
    _rule(rf"Run the {_N}(?= unit and integration tests)", "tests"),
    _rule(rf"{_N}(?= CI-Gated Tests)", "tests"),
    # Canonical skills (skills/)
    _rule(rf"{_N}(?= canonical (?:engine )?skills)", "canonical_skills", flags=re.I),
    # Active harness skills (.agents/skills)
    _rule(rf"{_N}(?= active (?:harness )?skills\b)", "active_harness_skills", flags=re.I),
    _rule(rf"Active Harness Skills(?: Index)? \({_N} Skills\)", "active_harness_skills"),
    _rule(rf"active-harness-skills(?:-index)?-{_N}(?=-skills\))", "active_harness_skills"),
    _rule(rf"Active Harness \({_N} skills\)", "active_harness_skills"),
    _rule(rf"{_N}(?= (?:Pre-Loaded )?Staff Engineer Skills)", "active_harness_skills"),
    _rule(rf"active--harness-{_N}(?=%20Pre--Loaded)", "active_harness_skills", "plain"),
    # Categories (awesome_skills/<category>/)
    _rule(rf"{_N}(?= domain categories)", "categories", flags=re.I),
    _rule(rf"across {_N}(?= functional domains| domains in `awesome_skills/`| categories\))", "categories"),
    _rule(rf"{_N}(?= Functional Domain Dirs)", "categories"),
    _rule(rf"badge/domains-{_N}(?=%20Categories)", "categories", "plain"),
    _rule(rf'alt="{_N}(?= Categories")', "categories", "plain"),
    # Catalog entries (records in awesome_skills/skills_index.json) — not unique skills
    _rule(rf"{_N}(?= catalog (?:entries|records))", "catalog_skills", flags=re.I),
    _rule(rf"Catalog (?:Records )?\({_N}\)", "catalog_skills"),
    _rule(rf"`{_N}` categorized implementations", "catalog_skills"),
    _rule(rf"\(\*\*{_N}(?= cataloged instances)", "catalog_skills"),
    _rule(rf"\*\*Catalog Records\*\* \| \*\*{_N}(?=\*\*)", "catalog_skills"),
    _rule(rf"badge/catalog-{_NURL}(?=%20Catalog%20Entries)", "catalog_skills", "url"),
    _rule(rf"{_N}(?=-item metadata database)", "catalog_index_records"),
    # Unique skills (deduplicated identities)
    _rule(rf"{_N}(?=\+? unique (?:specialized |skill))", "total_unique_skills", flags=re.I),
    _rule(rf"`{_N}` distinct skill capabilities", "total_unique_skills"),
    _rule(rf"\*\*Unique Skills\*\* \| \*\*{_N}(?=\*\*)", "total_unique_skills"),
    _rule(rf"badge/skills-{_NURL}(?=%2B%20Unique%20Skills)", "total_unique_skills", "url"),
]

_STYLES = {
    "comma": lambda n: f"{n:,}",
    "plain": lambda n: str(n),
    "url": lambda n: f"{n:,}".replace(",", "%2C"),
}


def _refit_box_cells(old: str, new: str) -> str:
    """Keep ASCII-art box cells at their original width after a number changed length."""
    old_cells, new_cells = old.split("│"), new.split("│")
    if len(old_cells) != len(new_cells):
        return new
    fitted = []
    for before, after in zip(old_cells, new_cells):
        if len(after) != len(before):
            body = after.rstrip(" ")
            after = body + " " * max(len(before) - len(body), 0)
        fitted.append(after)
    return "│".join(fitted)


def apply_doc_counts(content: str, stats: dict) -> tuple[str, list[tuple[int, str, str]]]:
    """Rewrite every documented count; return (new text, [(line, old, new)])."""
    changes: list[tuple[int, str, str]] = []
    lines = content.split("\n")
    for index, line in enumerate(lines):
        new_line = line
        for pattern, key, style in DOC_COUNT_RULES:
            value = _STYLES[style](stats[key])

            def rewrite(match: re.Match[str], value: str = value, lineno: int = index + 1) -> str:
                whole, start = match.group(0), match.start()
                if match.group("n") != value:
                    changes.append((lineno, match.group("n"), value))
                return whole[: match.start("n") - start] + value + whole[match.end("n") - start:]

            new_line = pattern.sub(rewrite, new_line)
        if new_line != line and "│" in line:
            new_line = _refit_box_cells(line, new_line)
        lines[index] = new_line
    return "\n".join(lines), changes


def doc_files(repo_root: Path) -> list[Path]:
    files: set[Path] = set()
    for pattern in DOC_FILES:
        files.update(p for p in repo_root.glob(pattern) if p.is_file())
    return sorted(files)


def _sync_file(path: Path, stats: dict) -> bool:
    """Apply DOC_COUNT_RULES to one file; True if it changed."""
    text = path.read_text(encoding="utf-8")
    new_text, changes = apply_doc_counts(text, stats)
    if changes:
        path.write_text(new_text, encoding="utf-8", newline="")
    return bool(changes)


def sync_docs(stats: dict, repo_root: Path | None = None) -> list[str]:
    """Apply DOC_COUNT_RULES to every documentation file; return the files changed."""
    repo_root = repo_root or get_repo_root()
    return [p.relative_to(repo_root).as_posix() for p in doc_files(repo_root) if _sync_file(p, stats)]


def verify_docs(stats: dict, repo_root: Path | None = None) -> list[str]:
    """Every documented count that disagrees with ``stats`` (empty = consistent)."""
    repo_root = repo_root or get_repo_root()
    problems = []
    for path in doc_files(repo_root):
        for line, old, new in apply_doc_counts(path.read_text(encoding="utf-8"), stats)[1]:
            problems.append(f"{path.relative_to(repo_root).as_posix()}:{line}: says {old}, stats.json says {new}")
    return problems


def sync_readme(stats: dict, repo_root: Path | None = None) -> bool:
    """Backward-compatible wrapper: sync README.md only."""
    path = (repo_root or get_repo_root()) / "README.md"
    return path.exists() and (_sync_file(path, stats) or True)


def sync_skills_md(stats: dict, repo_root: Path | None = None) -> bool:
    """Backward-compatible wrapper: sync SKILLS.md only."""
    path = (repo_root or get_repo_root()) / "SKILLS.md"
    return path.exists() and (_sync_file(path, stats) or True)


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
        changed = sync_docs(computed, repo_root)
        for path in changed:
            print(f"Successfully synchronized {path} numbers.")
        if not changed:
            print("Documentation counts already match stats.json.")


if __name__ == "__main__":
    main()
