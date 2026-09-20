#!/usr/bin/env python3
"""Pre-execution hook: check environment readiness.

Verifies:
- Python 3.9+ runtime
- Virtual environment active or available
- Git executable available
"""
from __future__ import annotations

import os
import shutil
import sys


def main() -> int:
    # 1. Python version check
    if sys.version_info < (3, 9):
        print(f"[PRE-HOOK:ENV] FAILED: Python >= 3.9 required, found {sys.version.split()[0]}", file=sys.stderr)
        return 1

    # 2. Virtual environment check
    in_venv = (
        hasattr(sys, "real_prefix") or
        (hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix) or
        bool(os.environ.get("VIRTUAL_ENV")) or
        bool(os.environ.get("CONDA_PREFIX"))
    )
    venv_status = "active" if in_venv else "system/global (warning: isolated venv recommended)"

    # 3. Required CLI tools
    git_bin = shutil.which("git")
    if not git_bin:
        print("[PRE-HOOK:ENV] WARNING: 'git' binary not found in PATH", file=sys.stderr)

    print(f"[PRE-HOOK:ENV] OK: Python {sys.version.split()[0]}, venv: {venv_status}, git: {'ok' if git_bin else 'missing'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
