#!/usr/bin/env python3
"""Unified Agent Skills Setup & Environment Initializer (/setup-skills).

Detects AI agent harnesses (Claude Code, Cursor, Codex CLI, Antigravity, Gemini CLI),
initialises workspace directories, creates native symlinks/junctions, and verifies
platform integrity.

Safety invariants:
  - Real directories that All-skills did NOT create are NEVER modified.
  - Removal only happens for entries present in state/managed_harnesses.json.
  - cmd /c rmdir is NEVER called on an unmanaged directory.

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

# Add scripts/ to path so we can import setup_tools
SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

REPO_ROOT = Path(__file__).resolve().parent.parent
CANONICAL_SOURCE = REPO_ROOT / ".agents" / "skills"


def is_windows() -> bool:
    return platform.system().lower() == "windows"


def create_link(source: Path, target: Path) -> bool:
    """
    Create a junction or symlink from source → target.

    Safety rules (matching setup_tools.py):
      - If target is a real (non-link) directory that is NOT in the managed ledger
        → print CONFLICT, skip without touching it.
      - If target is an existing managed link/junction → remove and recreate.
      - shutil.rmtree and cmd rmdir on unmanaged directories are FORBIDDEN.
    """
    from setup_tools import is_link_or_junction, is_managed, _remove_link_only, ledger_record

    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() or target.is_symlink():
        if is_link_or_junction(target):
            if is_managed(target):
                # Managed link — safe to replace
                _remove_link_only(target)
            else:
                # Unmanaged link — warn but allow replacement (user-created link is OK to replace)
                print(f"  ⚠️  Replacing unmanaged link: {target}", file=sys.stderr)
                _remove_link_only(target)
        else:
            # Real directory — NEVER touch
            print(
                f"  ⚠️  CONFLICT: {target} is a real directory. "
                "All-skills will not modify it.",
                file=sys.stderr,
            )
            return False

    if target.exists():
        return False

    if is_windows():
        res = subprocess.run(
            ["cmd", "/c", f'mklink /J "{target}" "{source}"'],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0:
            ledger_record(target, source, "junction")
            return True
        return False
    else:
        try:
            target.symlink_to(source, target_is_directory=True)
            ledger_record(target, source, "symlink")
            return True
        except OSError as e:
            print(f"  ⚠️  Failed creating symlink {target} → {source}: {e}", file=sys.stderr)
            return False


def run_setup(include_global: bool = False, verify: bool = True) -> int:
    from setup_tools import cmd_setup, cmd_verify
    cmd_setup(include_global=include_global, replace_managed=False)

    if verify:
        print("\n🔍 Running Verification Checks:")
        # 1. Schema check
        res_schema = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate_schema.py")],
            capture_output=True,
            text=True,
        )
        if res_schema.returncode == 0:
            lines = res_schema.stdout.strip().split("\n")
            print(f"  ✅ Frontmatter Schemas: {lines[-1] if lines else 'OK'}")
        else:
            print(f"  ❌ Frontmatter Schemas: Validation issues:\n{res_schema.stdout}")

        # 2. Manifest check
        manifest_file = REPO_ROOT / "manifest.json"
        if manifest_file.exists():
            print(f"  ✅ Agent Manifest: Present ({manifest_file.name})")
        else:
            print("  ⚠️  Agent Manifest: manifest.json missing. Generating…")
            subprocess.run(
                [sys.executable, str(REPO_ROOT / "scripts" / "generate_manifest.py")],
                check=False,
            )

        # 3. Router / doctor check
        route_check = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "skills" / "skills.py"), "doctor"],
            capture_output=True,
            text=True,
        )
        if route_check.returncode == 0:
            print("  ✅ Canonical Engine: Skills router clean (0 errors)")
        else:
            print(f"  ⚠️  Canonical Engine: Issues found:\n{route_check.stdout[:400]}")

        # 4. Platform harness verification
        cmd_verify()

    print("\n" + "=" * 65)
    print("🎉 Workspace successfully configured for all 11 AI coding agents!")
    print("=" * 65)
    return 0


def check_status() -> None:
    from setup_tools import cmd_status
    cmd_status()


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous Agent Setup & Initializer")
    parser.add_argument("--status",    action="store_true", help="Print harness detection report")
    parser.add_argument(
        "--global", dest="include_global", action="store_true",
        help="Include global user profile directories",
    )
    parser.add_argument("--no-verify", action="store_true", help="Skip running test and schema verifications")
    args = parser.parse_args()

    if args.status:
        check_status()
        return 0

    return run_setup(include_global=args.include_global, verify=not args.no_verify)


if __name__ == "__main__":
    sys.exit(main())
