#!/usr/bin/env python3
"""Normalize local SKILL.md files without replacing their existing guidance."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skills.frontmatter import parse_frontmatter  # noqa: E402

REQUIRED = [
    "Purpose", "When to Use", "When NOT to Use", "Capabilities", "Inputs",
    "Workflow", "Tools", "Examples", "Safety", "Source", "Notes",
]


def section_text(section: str, meta: dict) -> str:
    name = str(meta.get("name", "this skill"))
    description = str(meta.get("description", "Perform the documented workflow."))
    triggers = meta.get("triggers", []) or []
    examples = "; ".join(f'"{item}"' for item in triggers[:3]) or f'"Use {name}."'
    values = {
        "Purpose": description,
        "When to Use": f"Use when the request matches the documented {name} capability or its declared triggers.",
        "When NOT to Use": "Do not use when the request is outside this capability, required context is unavailable, or a safer specialized skill applies.",
        "Capabilities": f"- Apply the {name} workflow consistently.\n- Produce a clear, reviewable result.\n- Surface assumptions, constraints, and unresolved risks.",
        "Inputs": "- The user's goal and desired output.\n- Relevant source material, constraints, and environment details.\n- Acceptance criteria when available.",
        "Workflow": "1. Confirm the goal, scope, and constraints.\n2. Inspect the available context before acting.\n3. Apply the skill-specific guidance in this document.\n4. Verify the result and report limitations or next steps.",
        "Tools": "- No mandatory tool unless declared in frontmatter.\n- Use only project-approved tools and documented optional dependencies.",
        "Examples": f"Requests that should activate this skill include: {examples}.",
        "Safety": "- Preserve user data and existing work.\n- Confirm before destructive or externally visible actions.\n- Do not expose credentials or claim unverified results.",
        "Source": "Custom skill maintained in this library unless otherwise stated in frontmatter and the source manifest.",
        "Notes": "This section was normalized to satisfy the library contract; retain more specific guidance elsewhere in this file.",
    }
    return f"## {section}\n\n{values[section]}\n"


def normalize(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    meta, _ = parse_frontmatter(text)
    headings = {m.group(1).strip().lower() for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)}
    missing = [section for section in REQUIRED if section.lower() not in headings]
    if missing:
        additions = "\n".join(section_text(section, meta) for section in missing)
        text = text.rstrip() + "\n\n" + additions
        path.write_text(text.rstrip() + "\n", encoding="utf-8")

    readme = path.parent / "README.md"
    if not readme.exists():
        category = meta.get("category", path.parent.parent.name)
        name = meta.get("name", path.parent.name)
        description = meta.get("description", "")
        readme.write_text(
            f"# {str(name).replace('-', ' ').title()}\n\n{description}\n\n"
            f"- **Skill ID:** `{category}.{name}`\n"
            f"- **Instructions:** [SKILL.md](SKILL.md)\n"
            f"- **Source:** See `../../SOURCES.json` for provenance and license details.\n",
            encoding="utf-8",
        )


def main() -> int:
    paths = [p for p in (ROOT / "skills").rglob("SKILL.md") if "_quarantine" not in p.parts]
    for path in sorted(paths):
        normalize(path)
    print(f"Normalized {len(paths)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
