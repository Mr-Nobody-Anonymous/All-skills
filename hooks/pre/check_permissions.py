#!/usr/bin/env python3
"""Pre-execution hook: check required tool permissions, environment variables, and enforce capability policy."""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

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

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.policy import PolicyEngine, PolicyVerdict


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", default="", help="Skill ID to verify")
    args = parser.parse_args()

    if not args.skill:
        print("[PRE-HOOK:PERMS] OK: No specific skill target provided, generic check passed.")
        return 0

    # 1. Check environment variables
    manifest_file = REPO_ROOT / "manifest.json"
    skill_data = {}
    if manifest_file.exists():
        try:
            with open(manifest_file, "r", encoding="utf-8") as f:
                manifest = json.load(f)
                skill_data = manifest.get("skills", {}).get(args.skill, {})
        except Exception as e:
            print(f"[PRE-HOOK:PERMS] WARNING: Could not read manifest.json: {e}", file=sys.stderr)

    missing_env = [env_var for env_var in skill_data.get("env", []) if not os.environ.get(env_var)]
    if missing_env:
        print(f"[PRE-HOOK:PERMS] FAILED: Missing required environment variable(s): {', '.join(missing_env)}", file=sys.stderr)
        return 1

    # 2. Capability Policy Engine Evaluation
    policy_engine = PolicyEngine(REPO_ROOT)
    tools = skill_data.get("tools", [])
    eval_result = policy_engine.evaluate_skill(args.skill, declared_tools=tools)

    if eval_result.overall_verdict == PolicyVerdict.DENY:
        print(f"[PRE-HOOK:PERMS] SECURITY POLICY DENIED for '{args.skill}':", file=sys.stderr)
        for reason in eval_result.reasons:
            print(f"  - {reason}", file=sys.stderr)
        return 1

    if eval_result.overall_verdict == PolicyVerdict.ASK:
        print(f"[PRE-HOOK:PERMS] WARNING: Skill '{args.skill}' requires elevated user confirmation ({eval_result.max_risk.value}):")
        for reason in eval_result.reasons:
            print(f"  [WARN] {reason}")
        return 0

    print(f"[PRE-HOOK:PERMS] OK: Permissions & capabilities ({', '.join(eval_result.capabilities_requested)}) pre-authorized for '{args.skill}'.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
