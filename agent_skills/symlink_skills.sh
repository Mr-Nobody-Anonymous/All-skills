#!/usr/bin/env bash
#===============================================================================
# symlink_skills.sh - attach every skill in ./skills/* to the active
# AI coding agent's global skills directory.
#===============================================================================
# Supported agents:
#   - Claude Code ........... ~/.claude/skills
#   - Codex ................. ~/.codex/skills
#   - OpenClaw .............. ~/.openclaw/skills
#
# Usage:
#   ./symlink_skills.sh                 auto-detect a target (or link to all)
#   ./symlink_skills.sh claude          only symlink into ~/.claude/skills
#   ./symlink_skills.sh codex           only symlink into ~/.codex/skills
#   ./symlink_skills.sh openclaw        only symlink into ~/.openclaw/skills
#   ./symlink_skills.sh all             symlink into every detected target
#   ./symlink_skills.sh --copy          use file copies instead of symlinks
#                                       (useful on Windows w/o Developer Mode)
#   ./symlink_skills.sh --cleanup claude|codex|openclaw
#                                       remove symlinks we previously created
#   ./symlink_skills.sh --cleanup-all
#                                       remove from all three targets
#   ./symlink_skills.sh --help          show this help
#
# Notes:
#   - On Windows, run from Git Bash or WSL. Symlinks require Developer Mode
#     or admin. The script falls back to a copy if `ln -s` fails.
#   - Skills without a `SKILL.md` are skipped with a warning.
#===============================================================================

set -euo pipefail

#-------------------------------------------------------------------------------
# Paths and defaults
#-------------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
SKILLS_DIR="${SCRIPT_DIR}/skills"
CLAUDE_SKILLS_PATH="${HOME}/.claude/skills"
CODEX_SKILLS_PATH="${HOME}/.codex/skills"
OPENCLAW_SKILLS_PATH="${HOME}/.openclaw/skills"
MARKER_FILE=".agent_skills_managed"

USE_COPY=0
TARGET_ARG=""

#-------------------------------------------------------------------------------
# Output helpers
#-------------------------------------------------------------------------------

if [ -t 1 ]; then
  RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'
  BLUE='\033[0;34m'; NC='\033[0m'
else
  RED=''; GREEN=''; YELLOW=''; BLUE=''; NC=''
fi

log_info()    { printf '%b[INFO]%b    %s\n' "$BLUE"   "$NC" "$1"; }
log_success() { printf '%b[OK]%b      %s\n' "$GREEN"  "$NC" "$1"; }
log_warning() { printf '%b[WARN]%b    %s\n' "$YELLOW" "$NC" "$1"; }
log_error()   { printf '%b[ERROR]%b   %s\n' "$RED"    "$NC" "$1" >&2; }


#-------------------------------------------------------------------------------
# Path resolution
#-------------------------------------------------------------------------------

resolve_target() {
  case "$1" in
    claude)   echo "$CLAUDE_SKILLS_PATH" ;;
    codex)    echo "$CODEX_SKILLS_PATH" ;;
    openclaw) echo "$OPENCLAW_SKILLS_PATH" ;;
    *)        return 1 ;;
  esac
}

detect_targets() {
  local hits=()
  for t in claude codex openclaw; do
    if [ -d "$(resolve_target "$t" 2>/dev/null || true)" ]; then
      hits+=("$t")
    fi
  done
  printf '%s\n' "${hits[@]}"
}

#-------------------------------------------------------------------------------
# Linking primitive
#-------------------------------------------------------------------------------

# Create a link at $2/$3 pointing to $1. Falls back to a recursive copy if
# symlinks are not supported (e.g. Windows without Developer Mode).
link_skill() {
  local src="$1" dst_dir="$2" name="$3"
  local dst="$dst_dir/$name"

  if [ ! -d "$src" ]; then
    log_warning "skip $name - source dir missing"
    return 1
  fi
  if [ ! -f "$src/SKILL.md" ]; then
    log_warning "skip $name - no SKILL.md"
    return 1
  fi

  mkdir -p "$dst_dir"

  if [ -L "$dst" ] || [ -e "$dst" ]; then
    rm -rf "$dst"
  fi

  if [ "$USE_COPY" -eq 0 ]; then
    if ln -s "$src" "$dst" 2>/dev/null; then
      log_success "linked  $name -> $dst"
      return 0
    fi
    log_warning "symlink failed for $name (try --copy on Windows) - falling back to copy"
  fi

  mkdir -p "$dst"
  (
    cd "$src"
    for f in ./* ./.[!.]*; do
      [ -e "$f" ] || continue
      bn=$(basename "$f")
      [ "$bn" = "." ] && continue
      [ "$bn" = ".." ] && continue
      cp -R "$f" "$dst/"
    done
  )
  log_success "copied  $name -> $dst"
  return 0
}

# Iterate every skill in skills/<category>/<skill>/ and link it.
link_all_into() {
  local target_dir="$1"
  local linked=0 skipped=0
  if [ ! -d "$SKILLS_DIR" ]; then
    log_error "skills dir not found: $SKILLS_DIR"
    return 1
  fi
  for category_dir in "$SKILLS_DIR"/*; do
    [ -d "$category_dir" ] || continue
    for skill_dir in "$category_dir"/*; do
      [ -d "$skill_dir" ] || continue
      local name
      name="$(basename "$skill_dir")"
      if link_skill "$skill_dir" "$target_dir" "$name"; then
        linked=$((linked + 1))
      else
        skipped=$((skipped + 1))
      fi
    done
  done
  : > "$target_dir/$MARKER_FILE"
  printf 'linked=%d skipped=%d\n' "$linked" "$skipped"
}



# Remove only the symlinks/copies we created (matched by name from SKILLS_DIR).
cleanup_target() {
  local target_dir="$1"
  if [ ! -d "$target_dir" ]; then
    log_warning "no such dir: $target_dir"
    return 0
  fi
  local removed=0
  [ -e "$target_dir/$MARKER_FILE" ] && rm -f "$target_dir/$MARKER_FILE"
  for category_dir in "$SKILLS_DIR"/*; do
    [ -d "$category_dir" ] || continue
    for skill_dir in "$category_dir"/*; do
      [ -d "$skill_dir" ] || continue
      local name
      name="$(basename "$skill_dir")"
      local link="$target_dir/$name"
      if [ -L "$link" ] || [ -d "$link" ]; then
        rm -rf "$link"
        log_info "removed $name"
        removed=$((removed + 1))
      fi
    done
  done
  printf 'removed=%d\n' "$removed"
}

print_help() {
  sed -n '2,30p' "$0" | sed 's/^# \{0,1\}//'
}

#-------------------------------------------------------------------------------
# Entry point
#-------------------------------------------------------------------------------

if [ $# -eq 0 ]; then
  TARGET_ARG="auto"
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --help|-h)        print_help; exit 0 ;;
    --copy)           USE_COPY=1 ;;
    --cleanup)
      shift
      target="${1:-}"
      if [ -z "$target" ]; then
        log_error "--cleanup requires an agent name: claude|codex|openclaw"
        exit 2
      fi
      cleanup_target "$(resolve_target "$target")"
      exit 0
      ;;
    --cleanup-all)
      for t in claude codex openclaw; do
        cleanup_target "$(resolve_target "$t")" >/dev/null || true
      done
      log_success "cleanup done"
      exit 0
      ;;
    claude|codex|openclaw|all|auto) TARGET_ARG="$1" ;;
    *)                log_error "unknown arg: $1"; print_help; exit 2 ;;
  esac
  shift
done

case "$TARGET_ARG" in
  auto)
    targets="$(detect_targets)"
    if [ -z "$targets" ]; then
      log_warning "no existing ~/.{claude,codex,openclaw}/skills dir found - symlinking to all three"
      targets="claude
codex
openclaw"
    fi
    ;;
  all) targets="claude
codex
openclaw" ;;
  *)   targets="$TARGET_ARG" ;;
esac

total_linked=0
total_skipped=0
for t in $targets; do
  target_dir="$(resolve_target "$t")"
  log_info "target: $t -> $target_dir"
  out="$(link_all_into "$target_dir")"
  log_info "$t summary: $out"
  linked=$(echo "$out" | sed -n 's/^linked=\([0-9]*\).*/\1/p')
  skipped=$(echo "$out" | sed -n 's/.*skipped=\([0-9]*\).*/\1/p')
  total_linked=$((total_linked + ${linked:-0}))
  total_skipped=$((total_skipped + ${skipped:-0}))
done

echo ""
log_success "done. linked=$total_linked skipped=$total_skipped"
log_info "restart your agent (or reload its skills) to pick up the new skills."

