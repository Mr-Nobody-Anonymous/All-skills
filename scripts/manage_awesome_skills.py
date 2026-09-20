#!/usr/bin/env python3
"""Awesome Skills Manager CLI.

Manage, search, inspect, and install from the 2,041+ categorized skills
in `awesome_skills/` into `.agents/skills/` (or custom harness paths).

Usage:
    python scripts/manage_awesome_skills.py list [--category <cat>]
    python scripts/manage_awesome_skills.py search <query> [--limit 20]
    python scripts/manage_awesome_skills.py info <skill-id>
    python scripts/manage_awesome_skills.py status
    python scripts/manage_awesome_skills.py install <skill-id-or-category> [--path <dir>]
    python scripts/manage_awesome_skills.py install-bundle <bundle-name> [--path <dir>]
"""
from __future__ import annotations

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

import argparse
import json
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AWESOME_DIR = ROOT / "awesome_skills"
DEFAULT_AGENTS_DIR = ROOT / ".agents" / "skills"
CATALOG_PATH = AWESOME_DIR / "skills_index.json"

BUNDLES = {
    "senior-engineer": [
        "brainstorming", "executing-plans", "concise-planning",
        "subagent-driven-development", "dispatching-parallel-agents",
        "using-git-worktrees", "verification-before-completion",
        "llm-prompt-optimizer", "code-showcase-systematic-debugging",
        "tdd", "code-reviewer", "code-review-excellence",
        "review-and-simplify-changes", "requesting-code-review",
        "receiving-code-review", "performance-profiling"
    ],
    "agentic-architect": [
        "multi-agent-architect", "multi-agent-patterns", "multi-agent-brainstorming",
        "agent-memory", "agent-memory-systems", "agent-evaluation",
        "context-window-management", "mcp-builder", "mcp-tool-developer",
        "agent-tool-builder", "ai-engineer", "ai-engineering-toolkit"
    ],
    "fullstack": [
        "design-system", "tailwind-design-system", "wcag-audit-patterns",
        "accessibility-compliance-accessibility-audit", "playwright-skill",
        "browser-automation", "browser-act", "react-state-management",
        "angular-state-management", "api-designer", "api-and-interface-design",
        "api-documentation", "database-design", "prisma-expert",
        "drizzle-orm-expert", "redis-cli"
    ],
    "devops-cloud": [
        "cloud-devops", "terraform-infrastructure", "ci-cd-and-automation",
        "kubernetes-architect", "kubernetes-deployment", "aws-serverless"
    ],
    "security": [
        "top-web-vulnerabilities", "sast-configuration", "security-scanning-security-sast",
        "vulnerability-scanner", "marketplace-rbac-audit", "secrets-management",
        "red-team-tactics"
    ],
    "saas-growth": [
        "saas-mvp-launcher", "micro-saas-launcher", "seo-geo", "copywriting",
        "email-sequence", "analytics-product", "changelog-automation",
        "pdf-official", "database-migration"
    ],
    "all-curated": [
        "brainstorming", "executing-plans", "concise-planning", "subagent-driven-development",
        "dispatching-parallel-agents", "using-git-worktrees", "verification-before-completion",
        "llm-prompt-optimizer", "code-showcase-systematic-debugging", "tdd",
        "code-reviewer", "code-review-excellence", "review-and-simplify-changes",
        "requesting-code-review", "receiving-code-review", "performance-profiling",
        "design-system", "tailwind-design-system", "wcag-audit-patterns",
        "accessibility-compliance-accessibility-audit", "playwright-skill",
        "browser-automation", "browser-act", "react-state-management",
        "angular-state-management", "api-designer", "api-and-interface-design",
        "api-documentation", "database-design", "prisma-expert", "drizzle-orm-expert",
        "redis-cli", "mcp-builder", "mcp-tool-developer", "ai-engineer",
        "ai-engineering-toolkit", "agent-memory", "agent-memory-systems",
        "agent-evaluation", "context-window-management", "multi-agent-architect",
        "multi-agent-patterns", "multi-agent-brainstorming", "agent-tool-builder",
        "cloud-devops", "terraform-infrastructure", "ci-cd-and-automation",
        "kubernetes-architect", "kubernetes-deployment", "aws-serverless",
        "top-web-vulnerabilities", "sast-configuration", "security-scanning-security-sast",
        "vulnerability-scanner", "marketplace-rbac-audit", "secrets-management",
        "red-team-tactics", "saas-mvp-launcher", "micro-saas-launcher", "seo-geo",
        "copywriting", "email-sequence", "analytics-product", "changelog-automation",
        "pdf-official", "database-migration"
    ]
}


def load_catalog() -> list[dict]:
    if not CATALOG_PATH.exists():
        print(f"Error: Catalog file not found at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def find_skill_on_disk(skill_id: str) -> tuple[Path | None, str | None]:
    for cat in os.listdir(AWESOME_DIR):
        cat_dir = AWESOME_DIR / cat
        if not cat_dir.is_dir():
            continue
        skill_dir = cat_dir / skill_id
        if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
            return skill_dir, cat
    return None, None


def cmd_list(args: argparse.Namespace) -> None:
    catalog = load_catalog()
    id_to_meta = {item["id"]: item for item in catalog}
    cats = sorted([c for c in os.listdir(AWESOME_DIR) if (AWESOME_DIR / c).is_dir()])

    if args.category:
        target_cat = args.category.strip().lower()
        if target_cat not in cats:
            print(f"Category '{target_cat}' not found. Available categories:")
            for c in cats[:20]:
                print(f"  - {c}")
            print(f"  ... ({len(cats)} total categories)")
            return
        cat_dir = AWESOME_DIR / target_cat
        skills = sorted([s for s in os.listdir(cat_dir) if (cat_dir / s).is_dir()])
        print(f"\n📂 Category: {target_cat} ({len(skills)} skills)\n")
        for s in skills:
            desc = id_to_meta.get(s, {}).get("description", "").replace("\n", " ").strip()
            if len(desc) > 80:
                desc = desc[:77] + "..."
            print(f"  • {s:35} {desc}")
        print()
        return

    print("\n📚 Available Categories in awesome_skills:\n")
    total = 0
    for c in cats:
        skills = [s for s in os.listdir(AWESOME_DIR / c) if (AWESOME_DIR / c / s).is_dir()]
        total += len(skills)
        print(f"  {c:30} : {len(skills):4d} skills")
    print(f"\nTotal: {total} skills across {len(cats)} categories.\n")
    print("Use --category <name> to list skills within a specific category.")


def cmd_search(args: argparse.Namespace) -> None:
    query = args.query.strip().lower()
    catalog = load_catalog()
    matches = []

    for item in catalog:
        s_id = item.get("id", "").lower()
        name = item.get("name", "").lower()
        desc = item.get("description", "").lower()
        cat = item.get("category", "").lower()

        score = 0
        if query == s_id:
            score += 100
        elif query in s_id:
            score += 50
        if query in name:
            score += 30
        if query in cat:
            score += 20
        if query in desc:
            score += 10

        if score > 0:
            matches.append((score, item))

    matches.sort(key=lambda x: -x[0])
    limit = args.limit or 20
    top = matches[:limit]

    print(f"\n🔍 Search results for '{query}' ({len(matches)} found, showing top {len(top)}):\n")
    for score, item in top:
        s_id = item.get("id")
        cat = item.get("category", "unknown")
        risk = item.get("risk", "unknown")
        desc = item.get("description", "").replace("\n", " ").strip()
        if len(desc) > 90:
            desc = desc[:87] + "..."
        print(f"  [{cat}] {s_id} (risk: {risk})\n      {desc}")
    print()


def cmd_info(args: argparse.Namespace) -> None:
    skill_id = args.skill_id.strip()
    skill_path, category = find_skill_on_disk(skill_id)

    catalog = load_catalog()
    id_to_meta = {item["id"]: item for item in catalog}
    meta = id_to_meta.get(skill_id, {})

    if not skill_path:
        print(f"Skill '{skill_id}' not found in awesome_skills.", file=sys.stderr)
        return

    skill_md = skill_path / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8") if skill_md.exists() else ""

    print(f"\n⚡ Skill: {skill_id}")
    print(f"📁 Category : {category}")
    print(f"🏷️ Risk     : {meta.get('risk', 'unknown')}")
    print(f"📍 Path     : {skill_path.relative_to(ROOT)}")
    print(f"📝 Summary  : {meta.get('description', '').strip()}")
    print("\n--- SKILL.md Preview (first 25 lines) ---\n")
    for line in content.splitlines()[:25]:
        print(" ", line)
    print("\n----------------------------------------\n")


def resolve_dest_dirs(args: argparse.Namespace) -> list[Path]:
    if getattr(args, "path", None):
        return [Path(args.path)]
    dirs = []
    if getattr(args, "claude", False):
        dirs.append(ROOT / ".claude" / "skills")
    if getattr(args, "cursor", False):
        dirs.append(ROOT / ".cursor" / "skills")
    if getattr(args, "codex", False):
        dirs.append(ROOT / ".codex" / "skills")
    if getattr(args, "antigravity", False):
        dirs.append(ROOT / ".agents" / "skills")
    if getattr(args, "all_tools", False):
        dirs = [
            ROOT / ".agents" / "skills",
            ROOT / ".claude" / "skills",
            ROOT / ".cursor" / "skills",
            ROOT / ".codex" / "skills",
        ]
    return dirs if dirs else [DEFAULT_AGENTS_DIR]


def cmd_status(args: argparse.Namespace) -> None:
    try:
        from setup_tools import cmd_status as tools_status
        tools_status()
    except Exception:
        target_dir = Path(args.path) if hasattr(args, "path") and args.path else DEFAULT_AGENTS_DIR
        if not target_dir.exists():
            print(f"No skills directory found at {target_dir}")
            return
        skills = sorted([s for s in os.listdir(target_dir) if (target_dir / s).is_dir()])
        print(f"\nActive Skills in {target_dir.relative_to(ROOT)} ({len(skills)} installed):\n")
        for i, s in enumerate(skills, 1):
            print(f"  {i:2d}. {s}")
        print()


def cmd_install(args: argparse.Namespace) -> None:
    target = args.target.strip()
    dest_dirs = resolve_dest_dirs(args)

    for dest_dir in dest_dirs:
        dest_dir.mkdir(parents=True, exist_ok=True)
        cat_dir = AWESOME_DIR / target.lower()
        if cat_dir.is_dir():
            skills = [s for s in os.listdir(cat_dir) if (cat_dir / s).is_dir()]
            print(f"Installing {len(skills)} skills from category '{target}' into {dest_dir.relative_to(ROOT)}...")
            for s in skills:
                src = cat_dir / s
                dst = dest_dir / s
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
            print(f"Successfully installed {len(skills)} skills.")
            continue

        skill_path, category = find_skill_on_disk(target)
        if skill_path:
            dst = dest_dir / target
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(skill_path, dst)
            print(f"Successfully installed '{target}' ({category}) into {dest_dir.relative_to(ROOT)}.")
            continue

        print(f"Error: '{target}' was not found as a skill ID or category.", file=sys.stderr)
        sys.exit(1)


def cmd_install_bundle(args: argparse.Namespace) -> None:
    bundle_name = args.bundle.strip().lower()
    if bundle_name not in BUNDLES:
        print(f"Unknown bundle '{bundle_name}'. Available bundles:", file=sys.stderr)
        for b in BUNDLES:
            print(f"  - {b} ({len(BUNDLES[b])} skills)", file=sys.stderr)
        sys.exit(1)

    dest_dirs = resolve_dest_dirs(args)
    skill_list = BUNDLES[bundle_name]

    for dest_dir in dest_dirs:
        dest_dir.mkdir(parents=True, exist_ok=True)
        print(f"Installing bundle '{bundle_name}' ({len(skill_list)} skills) into {dest_dir.relative_to(ROOT)}...")
        installed = 0
        missing = []

        for s_id in skill_list:
            skill_path, _ = find_skill_on_disk(s_id)
            if skill_path:
                dst = dest_dir / s_id
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(skill_path, dst)
                installed += 1
            else:
                missing.append(s_id)

        print(f"Installed {installed} skills successfully into {dest_dir.relative_to(ROOT)}.")
        if missing:
            print(f"Warning: {len(missing)} skills could not be found: {', '.join(missing)}")


def cmd_setup_tools(args: argparse.Namespace) -> None:
    try:
        from setup_tools import cmd_setup
        cmd_setup(include_global=getattr(args, "is_global", False))
    except Exception as e:
        print(f"Error during harness setup: {e}", file=sys.stderr)


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage Awesome Skills library")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser("list", help="List categories or skills in a category")
    p_list.add_argument("--category", "-c", help="Filter by category")

    # search
    p_search = subparsers.add_parser("search", help="Search skills by keyword")
    p_search.add_argument("query", help="Search query")
    p_search.add_argument("--limit", "-l", type=int, default=20, help="Maximum results to return")

    # info
    p_info = subparsers.add_parser("info", help="Show detailed info about a skill")
    p_info.add_argument("skill_id", help="Exact skill ID")

    # status
    p_status = subparsers.add_parser("status", help="Show active skills across all harnesses")
    p_status.add_argument("--path", help="Custom harness skills directory")

    # setup-tools
    p_setup = subparsers.add_parser("setup-tools", help="Link skills to Claude Code, Cursor, Codex, and Antigravity")
    p_setup.add_argument("--global", dest="is_global", action="store_true", help="Also link user home directories")

    # install
    p_install = subparsers.add_parser("install", help="Install a skill or category into agent skills")
    p_install.add_argument("target", help="Skill ID or category name to install")
    p_install.add_argument("--path", help="Destination path (default: .agents/skills)")
    p_install.add_argument("--claude", action="store_true", help="Target .claude/skills")
    p_install.add_argument("--cursor", action="store_true", help="Target .cursor/skills")
    p_install.add_argument("--codex", action="store_true", help="Target .codex/skills")
    p_install.add_argument("--antigravity", action="store_true", help="Target .agents/skills")
    p_install.add_argument("--all-tools", action="store_true", help="Target all connected harnesses")

    # install-bundle
    p_bundle = subparsers.add_parser("install-bundle", help="Install a pre-configured skill bundle")
    p_bundle.add_argument("bundle", choices=list(BUNDLES.keys()), help="Bundle name")
    p_bundle.add_argument("--path", help="Destination path (default: .agents/skills)")
    p_bundle.add_argument("--claude", action="store_true", help="Target .claude/skills")
    p_bundle.add_argument("--cursor", action="store_true", help="Target .cursor/skills")
    p_bundle.add_argument("--codex", action="store_true", help="Target .codex/skills")
    p_bundle.add_argument("--antigravity", action="store_true", help="Target .agents/skills")
    p_bundle.add_argument("--all-tools", action="store_true", help="Target all connected harnesses")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args)
    elif args.command == "search":
        cmd_search(args)
    elif args.command == "info":
        cmd_info(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "setup-tools":
        cmd_setup_tools(args)
    elif args.command == "install":
        cmd_install(args)
    elif args.command == "install-bundle":
        cmd_install_bundle(args)


if __name__ == "__main__":
    main()
