#!/usr/bin/env python3
"""Manage Skill Packs (Bundles) for AI Agent Harnesses.

Usage:
    python scripts/manage_packs.py list
    python scripts/manage_packs.py info <pack-name>
    python scripts/manage_packs.py install <pack-name> [--target all|claude|cursor|codex|agents]
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
PACKS_FILE = REPO_ROOT / "packs" / "packs.json"
ACTIVE_SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
AWESOME_SKILLS_DIR = REPO_ROOT / "awesome_skills"


def load_packs() -> dict:
    if not PACKS_FILE.exists():
        print(f"Error: {PACKS_FILE} not found.", file=sys.stderr)
        sys.exit(1)
    with open(PACKS_FILE, "r", encoding="utf-8") as f:
        return json.load(f).get("packs", {})


def cmd_list() -> None:
    packs = load_packs()
    print("=" * 65)
    print("📦 CURATED AGENT SKILL PACKS (BUNDLES)")
    print("=" * 65)
    for pack_id, data in packs.items():
        skills = data.get("skills", [])
        print(f"\n📦 {data.get('name')} (`{pack_id}`)")
        print(f"   Description: {data.get('description')}")
        print(f"   Skills ({len(skills)}): {', '.join(skills[:5])}{'...' if len(skills) > 5 else ''}")
        print(f"   Recommended Workflow: {data.get('recommended_workflow', 'none')}")
    print("\n" + "=" * 65)
    print("Install a pack with: python scripts/manage_packs.py install <pack-name>")


def cmd_info(pack_name: str) -> None:
    packs = load_packs()
    pack = packs.get(pack_name)
    if not pack:
        print(f"Error: Pack '{pack_name}' not found. Available: {', '.join(packs.keys())}", file=sys.stderr)
        sys.exit(1)

    print("=" * 65)
    print(f"📦 SKILL PACK: {pack.get('name').upper()} (`{pack_name}`)")
    print(f"Description: {pack.get('description')}")
    print(f"Category: {pack.get('category')}")
    print(f"Recommended Workflow: {pack.get('recommended_workflow')}")
    print("=" * 65)
    print("\nIncluded Skills:")
    for skill_name in pack.get("skills", []):
        active_path = ACTIVE_SKILLS_DIR / skill_name
        is_active = active_path.exists()
        status_str = "✅ In Active Harness" if is_active else "⚪ In Awesome Library"
        print(f"  • {skill_name:<35} : {status_str}")


def cmd_install(pack_name: str, target: str = "all") -> None:
    packs = load_packs()
    pack = packs.get(pack_name)
    if not pack:
        print(f"Error: Pack '{pack_name}' not found.", file=sys.stderr)
        sys.exit(1)

    print(f"Installing Skill Pack '{pack.get('name')}' ({len(pack.get('skills', []))} skills)...")
    installed_count = 0

    for skill_name in pack.get("skills", []):
        dest_dir = ACTIVE_SKILLS_DIR / skill_name
        if dest_dir.exists():
            continue
        # Search in awesome_skills
        found_path = None
        for cand in AWESOME_SKILLS_DIR.rglob(skill_name):
            if cand.is_dir() and (cand / "SKILL.md").exists():
                found_path = cand
                break
        if found_path:
            shutil.copytree(found_path, dest_dir)
            installed_count += 1
            print(f"  + Installed: {skill_name}")

    print(f"Done! Pack '{pack_name}' is active ({len(pack.get('skills', []))} skills available).")


def main() -> int:
    parser = argparse.ArgumentParser(description="Agent Skill Packs Manager")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list")

    info_p = sub.add_parser("info")
    info_p.add_argument("pack_name")

    inst_p = sub.add_parser("install")
    inst_p.add_argument("pack_name")
    inst_p.add_argument("--target", default="all", choices=["all", "claude", "cursor", "codex", "agents"])

    args = parser.parse_args()

    if args.command == "list":
        cmd_list()
    elif args.command == "info":
        cmd_info(args.pack_name)
    elif args.command == "install":
        cmd_install(args.pack_name, args.target)
    else:
        cmd_list()
    return 0


if __name__ == "__main__":
    sys.exit(main())
