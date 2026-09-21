#!/bin/bash
# Run the full All-Skills test suite.
# Usage: bash scripts/run_tests.sh [--fast] [--verbose]

set -e
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "====================================="
echo " All-Skills Platform Test Suite"
echo "====================================="

echo ""
echo "[1/3] Frontmatter Schema Validation..."
python scripts/validate_schema.py

echo ""
echo "[2/3] Main Test Suite..."
python scripts/skills/skills.py test

echo ""
echo "[3/3] Unit Tests Discovery..."
python -m unittest discover -s tests -v

echo ""
echo "====================================="
echo " All tests completed."
echo "====================================="
