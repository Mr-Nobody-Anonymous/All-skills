#!/usr/bin/env python3
"""Post-execution hook: AST and syntax verification on workspace changes.

Ensures that files modified during agent execution are syntactically valid
and do not contain broken syntax or incomplete edits.
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def get_modified_files() -> list[str]:
    try:
        res = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            check=True
        )
        files = []
        for line in res.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            # status like " M path" or "?? path"
            parts = line.split(maxsplit=1)
            if len(parts) == 2:
                files.append(parts[1])
        return files
    except Exception:
        return []


def verify_python(path: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        ast.parse(content, filename=str(path))
        return None
    except SyntaxError as e:
        return f"Python SyntaxError in {path.name}: {e}"
    except Exception as e:
        return f"Error reading {path.name}: {e}"


def verify_json(path: Path) -> str | None:
    try:
        content = path.read_text(encoding="utf-8", errors="replace")
        json.loads(content)
        return None
    except json.JSONDecodeError as e:
        return f"JSON ParseError in {path.name}: {e}"
    except Exception as e:
        return f"Error reading {path.name}: {e}"


def main() -> int:
    files = get_modified_files()
    errors = []

    for rel_path in files:
        full_path = REPO_ROOT / rel_path
        if not full_path.exists() or not full_path.is_file():
            continue
        if full_path.suffix == ".py":
            err = verify_python(full_path)
            if err:
                errors.append(err)
        elif full_path.suffix == ".json":
            err = verify_json(full_path)
            if err:
                errors.append(err)

    if errors:
        print("[POST-HOOK:SYNTAX] FAILED: Syntax verification failed on modified files:", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"[POST-HOOK:SYNTAX] OK: Syntax valid across {len(files)} modified file(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
