#!/usr/bin/env python3
"""On-failure hook: evaluates error fingerprint, prevents loops, and manages recovery."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_DIR = REPO_ROOT / ".agents" / "state"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skill", default="unknown", help="Skill ID that failed")
    parser.add_argument("--error", default="", help="Error message / failure output")
    parser.add_argument("--rollback", action="store_true", help="Force git rollback to baseline")
    args = parser.parse_args()

    STATE_DIR.mkdir(parents=True, exist_ok=True)
    history_file = STATE_DIR / "error_history.json"
    
    history = []
    if history_file.exists():
        try:
            with open(history_file, "r", encoding="utf-8") as f:
                history = json.load(f)
        except Exception:
            history = []

    err_text = args.error.strip()
    err_hash = hashlib.sha256(err_text.encode("utf-8")).hexdigest()[:12] if err_text else "none"

    # Count consecutive identical error fingerprints
    consecutive_repeats = 0
    for prev in reversed(history):
        if prev.get("hash") == err_hash and prev.get("skill") == args.skill:
            consecutive_repeats += 1
        else:
            break

    entry = {
        "skill": args.skill,
        "hash": err_hash,
        "error_snippet": err_text[:200]
    }
    history.append(entry)
    with open(history_file, "w", encoding="utf-8") as f:
        json.dump(history[-20:], f, indent=2)

    # Loop Detection: 2 consecutive identical errors = infinite loop risk!
    if consecutive_repeats >= 2:
        print(
            f"[ON-FAILURE:LOOP-BREAKER] CRITICAL: Infinite error loop detected! "
            f"Error hash '{err_hash}' repeated {consecutive_repeats + 1} times for '{args.skill}'. "
            f"Halting execution immediately to protect tokens and workspace.",
            file=sys.stderr
        )
        return 2

    # Handle rollback if requested
    if args.rollback:
        baseline_file = STATE_DIR / "baseline_sha.txt"
        if baseline_file.exists():
            sha = baseline_file.read_text(encoding="utf-8").strip()
            print(f"[ON-FAILURE:RECOVERY] Rolling back workspace to baseline commit {sha[:8]}...")
            subprocess.run(["git", "reset", "--hard", sha], cwd=str(REPO_ROOT), check=False)

    print(f"[ON-FAILURE:RECOVERY] Recorded failure for '{args.skill}' (fingerprint: {err_hash}). Consecutive: {consecutive_repeats + 1}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
