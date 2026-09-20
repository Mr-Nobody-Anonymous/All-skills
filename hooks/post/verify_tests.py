#!/usr/bin/env python3
"""Post-execution hook: run platform regression unit tests."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main() -> int:
    try:
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "skills" / "skills.py"), "test"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True
        )
        if res.returncode == 0:
            print("[POST-HOOK:TESTS] OK: All unit tests passed.")
            return 0
        else:
            print("[POST-HOOK:TESTS] FAILED: Unit tests failed after execution:", file=sys.stderr)
            print(res.stderr or res.stdout, file=sys.stderr)
            return res.returncode
    except Exception as e:
        print(f"[POST-HOOK:TESTS] ERROR: Failed running tests: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
