#!/usr/bin/env python3
"""Universal Multi-Tool Agent Harness Setup.

Connects the active skills library to all major AI coding agent tools:
  - Antigravity / Gemini CLI (.agents/skills)
  - Claude Code (.claude/skills)
  - Cursor (.cursor/skills)
  - Codex CLI (.codex/skills)
  - Optional: Global user directories (~/.claude/skills, ~/.cursor/skills, etc.)

Usage:
    python scripts/setup_tools.py                # Set up local workspace harnesses
    python scripts/setup_tools.py --status       # Check health & detection across all tools
    python scripts/setup_tools.py --global       # Also link/sync to user profile directories
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
import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_SKILLS = ROOT / ".agents" / "skills"
HOME = Path.home()

LOCAL_TARGETS = {
    "Antigravity / Gemini CLI": ROOT / ".agents" / "skills",
    "Claude Code": ROOT / ".claude" / "skills",
    "Cursor": ROOT / ".cursor" / "skills",
    "Codex CLI": ROOT / ".codex" / "skills",
}

GLOBAL_TARGETS = {
    "Claude Code (User Global)": HOME / ".claude" / "skills",
    "Cursor (User Global)": HOME / ".cursor" / "skills",
    "Codex CLI (User Global)": HOME / ".codex" / "skills",
    "Antigravity / Agents (User Global)": HOME / ".agents" / "skills",
    "Antigravity CLI Slash Commands": HOME / ".gemini" / "antigravity-cli" / "skills",
}


def link_or_copy(src: Path, dst: Path) -> bool:
    if dst.exists():
        return True

    dst.parent.mkdir(parents=True, exist_ok=True)

    # On Windows, try junction first (does not require admin privileges)
    if os.name == "nt":
        try:
            import _winapi
            _winapi.CreateJunction(str(src), str(dst))
            return True
        except Exception:
            pass

    # Try standard symlink
    try:
        os.symlink(str(src), str(dst), target_is_directory=True)
        return True
    except Exception:
        pass

    # Fallback: copy tree
    try:
        shutil.copytree(src, dst)
        return True
    except Exception as e:
        print(f"Failed to link or copy {src} -> {dst}: {e}", file=sys.stderr)
        return False


def cmd_status() -> None:
    print("\n🔍 AI Coding Agent Harness Status:\n")
    print(f"Source canonical harness: {SOURCE_SKILLS.relative_to(ROOT)} ({len(os.listdir(SOURCE_SKILLS)) if SOURCE_SKILLS.exists() else 0} skills)\n")

    print("📁 Local Workspace Targets:")
    for name, path in LOCAL_TARGETS.items():
        exists = path.exists()
        count = len(os.listdir(path)) if exists and path.is_dir() else 0
        status = f"✅ Active ({count} skills)" if exists and count > 0 else "❌ Not linked"
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"  • {name:28} -> {str(rel):20} : {status}")

    print("\n🌐 Global User Profile Targets:")
    for name, path in GLOBAL_TARGETS.items():
        exists = path.exists()
        count = len(os.listdir(path)) if exists and path.is_dir() else 0
        status = f"✅ Active ({count} skills)" if exists and count > 0 else "⚪ Not configured"
        print(f"  • {name:32} -> {str(path):35} : {status}")
    print()


def cmd_setup(include_global: bool = False) -> None:
    if not SOURCE_SKILLS.exists():
        print(f"Error: Source skills directory not found at {SOURCE_SKILLS}", file=sys.stderr)
        sys.exit(1)

    print("\n⚡ Setting up Local Workspace AI Agent Harnesses...\n")
    for name, dst in LOCAL_TARGETS.items():
        if dst == SOURCE_SKILLS:
            continue
        success = link_or_copy(SOURCE_SKILLS, dst)
        count = len(os.listdir(dst)) if dst.exists() and dst.is_dir() else 0
        mark = "✅ Linked" if success else "❌ Failed"
        print(f"  {mark:10} {name:25} -> {dst.relative_to(ROOT)} ({count} skills)")

    if include_global:
        print("\n🌐 Setting up Global User Profile Harnesses...\n")
        for name, dst in GLOBAL_TARGETS.items():
            success = link_or_copy(SOURCE_SKILLS, dst)
            count = len(os.listdir(dst)) if dst.exists() and dst.is_dir() else 0
            mark = "✅ Linked" if success else "❌ Failed"
            print(f"  {mark:10} {name:32} -> {dst} ({count} skills)")

    print("\n🎉 Multi-tool setup complete! All agents can now discover and load active skills.\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Tool Agent Harness Setup")
    parser.add_argument("--status", action="store_true", help="Inspect status of tool harnesses")
    parser.add_argument("--global", dest="is_global", action="store_true", help="Also link to user home directories")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    else:
        cmd_setup(include_global=args.is_global)


if __name__ == "__main__":
    main()
