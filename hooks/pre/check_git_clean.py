#!/usr/bin/env python3
"""Pre-execution hook: snapshot workspace state & Git commit SHA."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
STATE_DIR = REPO_ROOT / ".agents" / "state"


def main() -> int:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    try:
        res = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True
        )
        head_sha = res.stdout.strip()
        (STATE_DIR / "baseline_sha.txt").write_text(head_sha, encoding="utf-8")
        
        status_res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        dirty = bool(status_res.stdout.strip())
        print(f"[PRE-HOOK:GIT] OK: Baseline SHA {head_sha[:8]} recorded. Dirty tree: {dirty}")
        return 0
    except Exception as e:
        print(f"[PRE-HOOK:GIT] WARNING: Git check skipped: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
