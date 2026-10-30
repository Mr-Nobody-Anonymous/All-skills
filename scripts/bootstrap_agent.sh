#!/usr/bin/env bash
# All-Skills one-command bootstrap for any agent harness.
#
# Does the three things a fresh machine needs:
#   1. links the canonical skill library into every detected harness,
#   2. installs a chosen MCP connector profile into the harness you name,
#   3. verifies both, and prints exactly what still needs credentials.
#
# Usage:
#   ./scripts/bootstrap_agent.sh                          # skills only, links + verify
#   ./scripts/bootstrap_agent.sh --harness cursor         # skills + core MCP for Cursor
#   ./scripts/bootstrap_agent.sh --harness claude --profile full
#   ./scripts/bootstrap_agent.sh --harness codex --profile standard --global
#   ./scripts/bootstrap_agent.sh --all --profile core     # every supported harness
#   ./scripts/bootstrap_agent.sh --harness vscode --dry-run
#
# Exit codes: 0 success, 1 a verification step failed, 2 bad usage.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PYTHON:-python3}"
HARNESS=""
PROFILE="core"
SCOPE="project"
GLOBAL_LINKS=0
DRY_RUN=0
ALL_HARNESSES=0
SKIP_SKILLS=0

usage() {
  sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --harness) HARNESS="${2:-}"; shift 2 ;;
    --profile) PROFILE="${2:-}"; shift 2 ;;
    --scope) SCOPE="${2:-}"; shift 2 ;;
    --all) ALL_HARNESSES=1; shift ;;
    --global) GLOBAL_LINKS=1; shift ;;
    --dry-run) DRY_RUN=1; shift ;;
    --skip-skills) SKIP_SKILLS=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage >&2; exit 2 ;;
  esac
done

if ! command -v "$PYTHON" >/dev/null 2>&1; then
  echo "ERROR: $PYTHON not found. Install Python >= 3.10 or set PYTHON=/path/to/python." >&2
  exit 2
fi

if [[ -z "$HARNESS" && $ALL_HARNESSES -eq 0 && $SKIP_SKILLS -eq 1 ]]; then
  echo "ERROR: --skip-skills needs --harness or --all." >&2
  exit 2
fi

cd "$ROOT"

echo "=============================================================="
echo " All-Skills bootstrap — $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo " workspace : $ROOT"
echo " python    : $("$PYTHON" --version 2>&1)"
echo "=============================================================="

if [[ $SKIP_SKILLS -eq 0 ]]; then
  echo
  echo "── 1/3  Linking the skill library into agent harnesses ──────"
  if [[ $DRY_RUN -eq 1 ]]; then
    "$PYTHON" scripts/setup_tools.py --status
  else
    "$PYTHON" scripts/setup_tools.py
    [[ $GLOBAL_LINKS -eq 1 ]] && "$PYTHON" scripts/setup_tools.py --global
  fi
fi

echo
echo "── 2/3  MCP connectors ───────────────────────────────────────"
if [[ $ALL_HARNESSES -eq 1 ]]; then
  mapfile -t HARNESS_LIST < <("$PYTHON" - <<'PY'
import json, pathlib
data = json.loads(pathlib.Path("mcps/catalog.json").read_text(encoding="utf-8"))
print("\n".join(sorted(data["harnesses"])))
PY
)
else
  HARNESS_LIST=("${HARNESS:-claude}")
fi

PLAN_FLAGS=()
[[ $DRY_RUN -eq 1 ]] && PLAN_FLAGS+=(--dry-run)

for target in "${HARNESS_LIST[@]}"; do
  echo
  echo "  → $target (profile: $PROFILE, scope: $SCOPE)"
  if ! "$PYTHON" scripts/mcp_catalog.py install \
      --harness "$target" --profile "$PROFILE" --scope "$SCOPE" "${PLAN_FLAGS[@]}"; then
    echo "  ! $target could not be configured (see the message above)" >&2
  fi
done

echo
echo "── 3/3  Verification ─────────────────────────────────────────"
status=0
"$PYTHON" scripts/setup_tools.py --verify || status=1
"$PYTHON" scripts/mcp_catalog.py verify || status=1
"$PYTHON" scripts/mcp_catalog.py doctor || status=1

echo
if [[ $status -eq 0 ]]; then
  echo "✅ Bootstrap complete."
  [[ $DRY_RUN -eq 1 ]] && echo "   (dry run — nothing was written)"
  echo "   Next: open your agent and run \`allskills mcp doctor\` to check credentials."
else
  echo "❌ Bootstrap finished with failures (see above)." >&2
fi
exit $status
