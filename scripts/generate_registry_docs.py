#!/usr/bin/env python3
"""Generate skills/registry.md, skills/SOURCES.json, skills/DEPENDENCIES.md
from the live registry and SKILL.md files.

Idempotent — overwrites the generated files with current data.
Run from repo root:
    python scripts/generate_registry_docs.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skills.registry import load_registry  # noqa: E402
from skills.frontmatter import parse_frontmatter  # noqa: E402
from skills.dependencies import check_dependency  # noqa: E402


def _workspace_root() -> Path:
    return ROOT


def _parse_license(skill_dir: Path) -> str | None:
    for candidate in ("LICENSE", "LICENSE.md", "LICENSE.txt", "license", "License"):
        p = skill_dir / candidate
        if p.exists():
            text = p.read_text(encoding="utf-8", errors="ignore").strip()
            first = text.splitlines()[0] if text else ""
            if "MIT" in text[:200]:
                return "MIT"
            if "Apache" in text[:200]:
                return "Apache-2.0"
            if "BSD" in text[:200]:
                return "BSD"
            return first[:80] or "unknown"
    return None


def _first_meaningful_line(body: str) -> str:
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("---"):
            return line
    return ""


def generate_registry_md(reg, out: Path) -> None:
    lines = ["# Skill Registry", ""]
    lines.append(f"_Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_")
    lines.append("")
    lines.append(f"**Total skills:** {len(reg.entries)}")
    lines.append("")
    cats = reg.categories()
    lines.append("| Category | Count |")
    lines.append("|---|---:|")
    for cat in sorted(cats):
        lines.append(f"| {cat} | {cats[cat]} |")
    lines.append("")

    for cat in sorted(cats):
        lines.append(f"## {cat}")
        lines.append("")
        lines.append("| ID | Risk | Description |")
        lines.append("|---|---|---|")
        for e in sorted(reg.by_category(cat), key=lambda x: x.id):
            desc = e.description.replace("|", "\\|")
            lines.append(f"| `{e.id}` | {e.risk} | {desc} |")
        lines.append("")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")


def generate_sources_json(reg, out: Path) -> None:
    skills_root = _workspace_root() / "skills"
    sources = {
        "version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "note": (
            "Imported skills are pinned to reviewed upstream commits. Custom skills are "
            "maintained locally. Third-party executables are not run during import."
        ),
        "skills": [],
    }
    for e in sorted(reg.entries, key=lambda x: x.id):
        skill_dir = skills_root / Path(*e.path.split("/"))
        license_ = _parse_license(skill_dir)
        skill_md = skill_dir / "SKILL.md"
        meta = {}
        if skill_md.exists():
            try:
                meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
            except Exception:
                meta = {}
        repository = meta.get("source_repository")
        sources["skills"].append({
            "skill": e.id,
            "repository": repository,
            "source_path": meta.get("source_path"),
            "commit": meta.get("source_commit"),
            "imported_at": meta.get("imported_at") if repository else None,
            "license": meta.get("license") or license_,
            "original_author": meta.get("original_author", "this-project"),
            "modified": str(meta.get("modified", "true")).lower() not in {"false", "no", "0"},
            "version": e.version,
            "source": e.source or "custom",
            "convention_referenced_from": ["agentskills/agentskills"],
        })
    out.write_text(json.dumps(sources, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {out}")


def generate_dependencies_md(reg, out: Path) -> None:
    skills_root = _workspace_root() / "skills"
    skill_with_deps = []
    skill_no_deps = []
    all_deps: Counter = Counter()
    for e in reg.entries:
        if e.dependencies:
            skill_with_deps.append(e)
            for d in e.dependencies:
                all_deps[d] += 1
        else:
            skill_no_deps.append(e)

    lines = [
        "# Skill Dependencies",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_",
        "",
        f"**Total skills:** {len(reg.entries)}",
        f"**Skills with declared dependencies:** {len(skill_with_deps)}",
        f"**Skills with no dependencies:** {len(skill_no_deps)}",
        "",
        "## Policy",
        "",
        "Per master prompt §14, dependencies are tracked but **not auto-installed**.",
        "Each skill that uses optional tooling lists its dependency here so the user",
        "can install on demand.",
        "",
        "Built-in capabilities (no install required):",
        "- Python 3.10+ standard library",
        "- The `src/skills/` loader/registry/router/validator library",
        "- The `scripts/skills/skills.py` CLI",
        "",
        "## Dependency Tally",
        "",
        "| Dependency | Skill Count |",
        "|---|---:|",
    ]
    for dep, n in sorted(all_deps.items(), key=lambda x: (-x[1], x[0])):
        lines.append(f"| `{dep}` | {n} |")
    if not all_deps:
        lines.append("| _(none declared)_ | — |")

    lines.append("")
    lines.append("## Per-Skill Status")
    lines.append("")
    lines.append("| Skill | Dependency | Required/Optional | Installation command | Platform | Status |")
    lines.append("|---|---|---|---|---|---|")
    install_commands = {
        "git": "Install Git from https://git-scm.com/downloads",
        "gh-cli": "Install GitHub CLI from https://cli.github.com/",
        "playwright": "npm install --save-dev playwright",
        "cypress": "npm install --save-dev cypress",
        "similar": "Install a supported browser automation tool",
    }
    for e in sorted(reg.entries, key=lambda x: x.id):
        if not e.dependencies:
            lines.append(f"| `{e.id}` | — | built-in | — | all | available |")
            continue
        for declaration in e.dependencies:
            status = check_dependency(e.id, declaration)
            normalized = declaration.removeprefix("optional:").removesuffix("-optional")
            candidates = [part for part in normalized.split("-or-") if part]
            commands = [install_commands.get(item, f"Install `{item}` per vendor documentation") for item in candidates]
            requirement = "optional" if status.optional else "required"
            availability = "available" if status.available else "missing"
            lines.append(
                f"| `{e.id}` | `{declaration}` | {requirement} | "
                f"{' or '.join(commands)} | all | {availability} |"
            )

    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")


def main() -> int:
    reg = load_registry(_workspace_root())
    skills_dir = _workspace_root() / "skills"
    skills_dir.mkdir(exist_ok=True)
    generate_registry_md(reg, skills_dir / "registry.md")
    generate_sources_json(reg, skills_dir / "SOURCES.json")
    generate_dependencies_md(reg, skills_dir / "DEPENDENCIES.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
