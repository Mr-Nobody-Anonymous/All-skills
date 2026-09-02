#!/usr/bin/env python3
"""Generate per-category docs in docs/skills/<category>.md from the live registry.

Idempotent — overwrites the generated files with current data.
Run from repo root:
    python scripts/generate_category_docs.py
"""
from __future__ import annotations

import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from skills.registry import load_registry  # noqa: E402
from skills.frontmatter import parse_frontmatter  # noqa: E402


CATEGORY_BLURB = {
    "productivity": (
        "Skills that help the user start, focus, plan, and finish — including "
        "ADHD-aware assistance, anti-procrastination, task decomposition, "
        "prioritization, and time management. The library intentionally leans on "
        "external, well-reviewed material (Cal Newport, James Clear, "
        "the Pomodoro technique, etc.) rather than inventing productivity "
        "philosophy from scratch."
    ),
    "development": (
        "Skills for software engineering work — coding, debugging, refactoring, "
        "code review, testing, TDD, architecture, frontend, backend, databases, "
        "Git, GitHub, performance optimization, and DevOps. These skills produce "
        "structured output (checklists, prompts, plans) rather than execute code."
    ),
    "research": (
        "Skills for finding, evaluating, and synthesizing information. Web "
        "research, deep research, academic research, fact checking, source "
        "verification, competitive analysis, and data analysis. All emphasize "
        "source diversification and citation discipline."
    ),
    "web": (
        "Skills that interact with the live web: browser automation, web "
        "scraping, web extraction, SEO audits, accessibility testing, and "
        "end-to-end website testing. These skills are wrappers around concrete "
        "tools (Playwright, Lighthouse-style checks, a11y linters) but the "
        "library itself is tooling-light — the skills describe the workflow."
    ),
    "documents": (
        "Skills for working with common document formats: PDF, DOCX, XLSX, "
        "PPTX, Markdown, and CSV. They focus on reliable extraction, "
        "structured generation, and content-aware summarization rather than "
        "format-perfect output."
    ),
    "design": (
        "Skills for design work — UI/UX, frontend design, presentations, and "
        "branding. These produce prose wireframes, design feedback, narrative "
        "arcs for talks, and naming/voice guidance."
    ),
    "security": (
        "Defensive security skills only: secure coding review, dependency "
        "auditing, secret detection, and prompt-injection defense. The "
        "library does not include any offensive security tooling."
    ),
    "utilities": (
        "General-purpose skills for working with files, text, images, and "
        "writing. Includes summarization, documentation generation, "
        "automation, and file management."
    ),
}


def _workspace_root() -> Path:
    return ROOT


def _first_paragraph(skill_md: Path) -> str:
    if not skill_md.exists():
        return ""
    try:
        meta, body = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    except Exception:
        return ""
    lines = []
    in_para = False
    for raw in body.splitlines():
        s = raw.strip()
        if not s:
            if in_para:
                break
            continue
        if s.startswith("#"):
            continue
        if s.startswith("---"):
            continue
        in_para = True
        lines.append(s)
    return " ".join(lines)[:400]


def _format_skill_block(e, skill_md: Path) -> str:
    excerpt = _first_paragraph(skill_md)
    aliases = ", ".join(f"`{a}`" for a in e.aliases) if e.aliases else "—"
    triggers = "\n".join(f"  - {t}" for t in (e.triggers or [])) or "  - _none_"
    return (
        f"### `{e.id}`\n\n"
        f"{e.description}\n\n"
        f"- **Risk:** {e.risk}\n"
        f"- **Path:** `{e.path}`\n"
        f"- **Aliases:** {aliases}\n"
        f"- **Triggers:**\n{triggers}\n"
        f"- **Source:** {e.source or 'custom'}\n"
        f"- **Version:** {e.version}\n\n"
        f"{excerpt}\n"
    )


def generate_category_doc(reg, category: str, out: Path) -> None:
    skills_root = _workspace_root() / "skills"
    entries = sorted(reg.by_category(category), key=lambda x: x.id)
    if not entries:
        return
    lines = [
        f"# {category.title()} Skills",
        "",
        f"_Generated: {datetime.now(timezone.utc).isoformat(timespec='seconds')}_",
        "",
        CATEGORY_BLURB.get(category, ""),
        "",
        f"**{len(entries)} skills in this category.**",
        "",
        "## Skills",
        "",
    ]
    for e in entries:
        skill_md = skills_root / Path(*e.path.split("/")) / "SKILL.md"
        lines.append(_format_skill_block(e, skill_md))
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {out}")


def main() -> int:
    reg = load_registry(_workspace_root())
    out_dir = _workspace_root() / "docs" / "skills"
    out_dir.mkdir(parents=True, exist_ok=True)
    # SECURITY.md (uppercase) is the hand-written security policy file and must
    # not be overwritten by the per-category generator. The category doc for
    # `security` lives at a separate path.
    for cat in sorted(set(CATEGORY_BLURB.keys()) | set(reg.categories().keys())):
        if reg.categories().get(cat, 0) <= 0:
            continue
        if cat == "security":
            out = out_dir / "security-category.md"
        else:
            out = out_dir / f"{cat}.md"
        generate_category_doc(reg, cat, out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
