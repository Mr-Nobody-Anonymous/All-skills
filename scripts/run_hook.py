#!/usr/bin/env python3
"""Unified Lifecycle Hook Runner for Autonomous Agent Harnesses.

Usage:
    python scripts/run_hook.py pre <skill_id>
    python scripts/run_hook.py post <skill_id>
    python scripts/run_hook.py failure <skill_id> --error "details"
    python scripts/run_hook.py list
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
HOOKS_CONFIG = REPO_ROOT / "hooks" / "hooks.json"


def load_hooks_config() -> dict:
    if not HOOKS_CONFIG.exists():
        print(f"Error: Hooks configuration not found at {HOOKS_CONFIG}", file=sys.stderr)
        sys.exit(1)
    with open(HOOKS_CONFIG, "r", encoding="utf-8") as f:
        return json.load(f)


def run_single_hook(script_rel_path: str, skill_id: str, extra_args: list[str], required: bool = False, security_critical: bool = False) -> int:
    script_path = REPO_ROOT / script_rel_path
    if not script_path.exists():
        if required or security_critical:
            print(f"[HOOKS] FATAL: Required security hook script not found: {script_path}", file=sys.stderr)
            return 1
        print(f"[HOOKS] Warning: Optional hook script not found: {script_path}", file=sys.stderr)
        return 0

    cmd = [sys.executable, str(script_path), "--skill", skill_id] + extra_args
    try:
        res = subprocess.run(cmd, cwd=str(REPO_ROOT), timeout=30)
        return res.returncode
    except subprocess.TimeoutExpired:
        print(f"[HOOKS] ERROR: Hook '{script_rel_path}' timed out after 30s", file=sys.stderr)
        return 124
    except Exception as e:
        print(f"[HOOKS] ERROR: Failed executing hook '{script_rel_path}': {e}", file=sys.stderr)
        return 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Autonomous Agent Lifecycle Hook Runner")
    parser.add_argument("stage", choices=["pre", "post", "failure", "list"], help="Lifecycle stage to run")
    parser.add_argument("skill", nargs="?", default="", help="Target skill ID")
    parser.add_argument("--error", default="", help="Error message if running failure stage")
    parser.add_argument("--rollback", action="store_true", help="Request rollback on failure")
    args = parser.parse_args()

    config = load_hooks_config()
    hooks_map = config.get("hooks", {})

    if args.stage == "list":
        print("Configured Lifecycle Hooks:")
        for stage_name, hooks in hooks_map.items():
            print(f"\n[{stage_name.upper()}]:")
            for h in hooks:
                req = "REQUIRED" if h.get("required") or h.get("security_critical") else "OPTIONAL"
                print(f"  - {h.get('id')} ({req}): {h.get('description')}")
        return 0

    stage_key = {
        "pre": "pre_execution",
        "post": "post_execution",
        "failure": "on_failure"
    }[args.stage]

    hooks_to_run = hooks_map.get(stage_key, [])
    print(f"[HOOKS] Running {len(hooks_to_run)} '{args.stage}' hook(s) for skill: {args.skill or 'workspace'}...")

    extra_args = []
    if args.error:
        extra_args.extend(["--error", args.error])
    if args.rollback:
        extra_args.append("--rollback")

    for hook in hooks_to_run:
        hook_id = hook.get("id")
        script_rel = hook.get("script")
        required = hook.get("required", False)
        security_critical = hook.get("security_critical", False)
        code = run_single_hook(script_rel, args.skill, extra_args, required=required, security_critical=security_critical)
        if code != 0:
            if required or security_critical:
                print(f"[HOOKS] ABORT: Required {args.stage} hook '{hook_id}' failed with exit code {code}", file=sys.stderr)
                return code
            else:
                print(f"[HOOKS] Warning: Optional {args.stage} hook '{hook_id}' exited with code {code}", file=sys.stderr)

    print(f"[HOOKS] All {args.stage} hooks completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
