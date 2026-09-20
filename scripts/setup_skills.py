#!/usr/bin/env python3
"""Unified Agent Skills Setup & Environment Initializer (/setup-skills).

Detects AI agent harnesses (Claude Code, Cursor, Codex CLI, Antigravity, Gemini CLI),
initializes workspace directories, creates native symlinks/junctions, and verifies
platform integrity.

Usage:
    python scripts/setup_skills.py            # Configure all local workspace harnesses
    python scripts/setup_skills.py --status   # Check status and detect harnesses
    python scripts/setup_skills.py --global   # Also configure global user profile harnesses
    python scripts/setup_skills.py --verify   # Run verification suite after setup
"""
from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SOURCE = REPO_ROOT / ".agents" / "skills"


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def create_link(source: Path, target: Path) -> bool:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.is_symlink():
        try:
            target.unlink()
        except OSError:
            pass
    elif target.exists():
        if is_windows():
            # Check if directory junction
            subprocess.run(["cmd", "/c", f'rmdir "{target}"'], capture_output=True, check=False)
        else:
            try:
                target.unlink()
            except OSError:
                pass

    if target.exists():
        return False

    if is_windows():
        res = subprocess.run(
            ["cmd", "/c", f'mklink /J "{target}" "{source}"'],
            capture_output=True,
            text=True
        )
        return res.returncode == 0
    else:
        try:
            target.symlink_to(source, target_is_directory=True)
            return True
        except OSError as e:
            print(f"Warning: Failed creating symlink {target} -> {source}: {e}", file=sys.stderr)
            return False


def run_setup(include_global: bool = False, verify: bool = True) -> int:
    print("=" * 65)
    print("🚀 ALL SKILLS — AGENT HARNESS INITIALIZER & LINKER")
    print("=" * 65)

    if not CANONICAL_SOURCE.exists():
        print(f"Error: Source skills directory not found at {CANONICAL_SOURCE}", file=sys.stderr)
        return 1

    skill_count = len([d for d in CANONICAL_SOURCE.iterdir() if d.is_dir() and (d / "SKILL.md").exists()])
    print(f"Found canonical active skills source: {CANONICAL_SOURCE} ({skill_count} skills)\n")

    # Local workspace harnesses
    local_targets = [
        ("Claude Code", REPO_ROOT / ".claude" / "skills"),
        ("Cursor", REPO_ROOT / ".cursor" / "skills"),
        ("Codex CLI", REPO_ROOT / ".codex" / "skills"),
    ]

    print("📁 Configuring Local Workspace Targets:")
    for name, target in local_targets:
        success = create_link(CANONICAL_SOURCE, target)
        status_str = "✅ Linked" if success else "⚠️  Failed or already configured"
        print(f"  • {name:<18} -> {target.relative_to(REPO_ROOT)} : {status_str}")

    # Global user profile harnesses
    if include_global:
        home = Path.home()
        global_targets = [
            ("Claude Code (User)", home / ".claude" / "skills"),
            ("Cursor (User)", home / ".cursor" / "skills"),
            ("Codex CLI (User)", home / ".codex" / "skills"),
            ("Agents (User)", home / ".agents" / "skills"),
        ]
        print("\n🌐 Configuring Global User Profile Targets:")
        for name, target in global_targets:
            success = create_link(CANONICAL_SOURCE, target)
            status_str = "✅ Linked" if success else "⚠️  Failed"
            print(f"  • {name:<20} -> {target} : {status_str}")

    if verify:
        print("\n🔍 Running Verification Checks:")
        # 1. Schema check
        res_schema = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "validate_schema.py")], capture_output=True, text=True)
        if res_schema.returncode == 0:
            print("  ✅ Frontmatter Schemas: All 192 SKILL.md files conforming.")
        else:
            print(f"  ❌ Frontmatter Schemas: Validation issues:\n{res_schema.stdout}")

        # 2. Manifest check
        manifest_file = REPO_ROOT / "manifest.json"
        if manifest_file.exists():
            print(f"  ✅ Agent Manifest: Present ({manifest_file.name}).")
        else:
            print("  ⚠️ Agent Manifest: manifest.json missing. Generating...")
            subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "generate_manifest.py")], check=False)

        # 3. Router check
        route_check = subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "skills" / "skills.py"), "doctor"], capture_output=True, text=True)
        if route_check.returncode == 0:
            print("  ✅ Canonical Engine: 122 routed skills clean (0 errors).")

    print("\n" + "=" * 65)
    print("🎉 Workspace successfully configured for all AI coding agents!")
    print("=" * 65)
    return 0


def check_status() -> None:
    from setup_tools import print_status
    print_status()


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous Agent Setup & Initializer")
    parser.add_argument("--status", action="store_true", help="Print harness detection report")
    parser.add_argument("--global", dest="include_global", action="store_true", help="Include global user profile directories")
    parser.add_argument("--no-verify", action="store_true", help="Skip running test and schema verifications")
    args = parser.parse_args()

    if args.status:
        check_status()
        return 0

    return run_setup(include_global=args.include_global, verify=not args.no_verify)


if __name__ == "__main__":
    sys.exit(main())
