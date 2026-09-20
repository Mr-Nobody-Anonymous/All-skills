#!/usr/bin/env bash
# ⚡ All Skills — Automated Environment & Harness Initializer
set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo "================================================================="
echo "⚡ ALL SKILLS — AGENT HARNESS INITIALIZER (/setup-skills)"
echo "================================================================="

# Detect python executable
if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
else
    echo "Error: Python 3.9+ is required but not found in PATH." >&2
    exit 1
fi

"$PYTHON_BIN" "$REPO_ROOT/scripts/setup_skills.py" "$@"
