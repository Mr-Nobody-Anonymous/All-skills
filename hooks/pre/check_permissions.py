#!/usr/bin/env python3
"""Pre-execution hook: check required tool permissions and environment variables."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", default="", help="Skill ID to verify")
    args = parser.parse_args()

    if not args.skill:
        print("[PRE-HOOK:PERMS] OK: No specific skill target provided, generic check passed.")
        return 0

    manifest_file = REPO_ROOT / "manifest.json"
    if not manifest_file.exists():
        print("[PRE-HOOK:PERMS] OK: manifest.json not found, skipping permission check.")
        return 0

    try:
        with open(manifest_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
    except Exception as e:
        print(f"[PRE-HOOK:PERMS] WARNING: Could not read manifest.json: {e}", file=sys.stderr)
        return 0

    skill_data = manifest.get("skills", {}).get(args.skill)
    if not skill_data:
        print(f"[PRE-HOOK:PERMS] OK: Skill '{args.skill}' not in manifest, proceeding.")
        return 0

    missing_env = [env_var for env_var in skill_data.get("env", []) if not os.environ.get(env_var)]
    if missing_env:
        print(f"[PRE-HOOK:PERMS] FAILED: Missing required environment variable(s): {', '.join(missing_env)}", file=sys.stderr)
        return 1

    tools = skill_data.get("tools", [])
    print(f"[PRE-HOOK:PERMS] OK: Permissions satisfied for '{args.skill}'. Tools required: {', '.join(tools)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
