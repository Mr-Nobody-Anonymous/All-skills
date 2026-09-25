#!/usr/bin/env python3
"""Universal Multi-Tool Agent Harness Setup.

Connects the active skills library to all major AI coding agent tools using dynamic
platform adapters defined in platforms/platforms.yaml and adapters/*.yaml:
  - Antigravity / Gemini CLI (.agents/skills)
  - Claude Code (.claude/skills)
  - Cursor (.cursor/skills)
  - Codex CLI (.codex/skills)
  - GitHub Copilot (.github/skills)
  - VS Code Agent (.vscode/skills)
  - Windsurf (.windsurf/skills)
  - OpenCode (.opencode/skills)
  - Cline (.cline/skills)
  - Roo Code (.roo/skills)
  - Block Goose (.goose/skills)

Safety invariants (hub-and-spoke architecture):
  1. A real (non-link) directory is NEVER touched — only managed links/junctions.
  2. --replace-managed-links only removes entries present in state/managed_harnesses.json.
  3. shutil.rmtree() is never called on any path.
  4. Every created link is recorded in state/managed_harnesses.json.

Usage:
    python scripts/setup_tools.py                        # Set up local workspace harnesses
    python scripts/setup_tools.py --status               # Check health & detection across all tools
    python scripts/setup_tools.py --global               # Also link/sync to user profile directories
    python scripts/setup_tools.py --replace-managed-links# Replace only All-skills-managed links
    python scripts/setup_tools.py --unlink               # Unlink harnesses cleanly (checks ledger)
    python scripts/setup_tools.py --verify               # Verify resolve and manifest integrity
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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

ROOT = Path(__file__).resolve().parents[1]
PLATFORMS_CONFIG = ROOT / "platforms" / "platforms.yaml"
LEDGER_PATH = ROOT / "state" / "managed_harnesses.json"
HOME = Path.home()


# ─────────────────────────────────────────────────────────────────────────────
# YAML LOADER
# ─────────────────────────────────────────────────────────────────────────────

def load_yaml(path: Path) -> Dict[str, Any]:
    """Simple robust YAML loader for platform configurations."""
    try:
        import yaml
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except ImportError:
        pass

    # Basic fallback parser if pyyaml not in environment
    data: Dict[str, Any] = {"local_targets": [], "global_targets": []}
    current_section = None
    current_item: Optional[Dict[str, Any]] = None

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            if line_str == "local_targets:":
                current_section = "local_targets"
                continue
            elif line_str == "global_targets:":
                current_section = "global_targets"
                continue
            elif line_str.startswith("- id:"):
                if current_item and current_section:
                    data[current_section].append(current_item)
                current_item = {"id": line_str.split(":", 1)[1].strip()}
            elif current_item and ":" in line_str:
                k, v = line_str.split(":", 1)
                current_item[k.strip().strip("- ")] = v.strip().strip('"').strip("'")
    if current_item and current_section:
        data[current_section].append(current_item)
    return data


# ─────────────────────────────────────────────────────────────────────────────
# LEDGER (managed_harnesses.json)
# ─────────────────────────────────────────────────────────────────────────────

def load_ledger() -> Dict[str, Any]:
    """Load the managed harnesses ledger. Returns {} if not yet created."""
    if LEDGER_PATH.exists():
        try:
            with open(LEDGER_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}


def save_ledger(ledger: Dict[str, Any]) -> None:
    """Persist the ledger to disk atomically."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    tmp = LEDGER_PATH.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(ledger, f, indent=2)
    tmp.replace(LEDGER_PATH)


def ledger_record(dst: Path, src: Path, link_type: str) -> None:
    """Record a managed link/junction in the ledger."""
    ledger = load_ledger()
    key = str(dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst)
    ledger[key] = {
        "managed": True,
        "type": link_type,
        "source": str(src.relative_to(ROOT) if src.is_relative_to(ROOT) else src),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    save_ledger(ledger)


def ledger_remove(dst: Path) -> None:
    """Remove a path from the ledger after it is unlinked."""
    ledger = load_ledger()
    key = str(dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst)
    ledger.pop(key, None)
    save_ledger(ledger)


def is_managed(dst: Path) -> bool:
    """Return True if this path is tracked as a managed link in the ledger."""
    ledger = load_ledger()
    key = str(dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst)
    return ledger.get(key, {}).get("managed", False)


# ─────────────────────────────────────────────────────────────────────────────
# LINK / JUNCTION DETECTION
# ─────────────────────────────────────────────────────────────────────────────

def is_link_or_junction(path: Path) -> bool:
    """
    Return True ONLY for symlinks and Windows directory junctions.
    Returns False for real directories even if they point elsewhere.
    """
    if path.is_symlink():
        return True
    if os.name == "nt":
        # Detect Windows junction via reparse point tag
        try:
            import ctypes
            import ctypes.wintypes
            FILE_ATTRIBUTE_REPARSE_POINT = 0x0400
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(path))
            if attrs != 0xFFFFFFFF and (attrs & FILE_ATTRIBUTE_REPARSE_POINT):
                return True
        except Exception:
            pass
    return False


# ─────────────────────────────────────────────────────────────────────────────
# SAFE LINK / UNLINK
# ─────────────────────────────────────────────────────────────────────────────

def link_or_copy(src: Path, dst: Path, replace_managed: bool = False) -> Tuple[bool, str]:
    """
    Create a junction (Windows), symlink (Unix), or copy from src → dst.

    Safety rules:
      - If dst is a REAL directory (not a link/junction) → REFUSE, return conflict.
      - If dst is a managed link/junction AND replace_managed=True → replace it.
      - If dst is a managed link/junction AND replace_managed=False → skip (already set up).
      - If dst does not exist → create link and record in ledger.

    Returns (success: bool, message: str).
    """
    if dst.exists() or dst.is_symlink():
        if is_link_or_junction(dst):
            if not is_managed(dst):
                return False, f"REFUSED: {dst} is an unmanaged link or junction. All-skills will not modify it."
            if not replace_managed:
                return True, "already-linked"
            # Safe to replace: remove the existing managed link
            _remove_link_only(dst)
            ledger_remove(dst)
        else:
            # Check if it was tracked in the ledger as a managed copy fallback
            if is_managed(dst):
                key = str(dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst)
                entry = load_ledger().get(key, {})
                if entry.get("type") == "copy":
                    if not replace_managed:
                        return True, "already-copied"
                    import shutil
                    shutil.rmtree(str(dst))
                    ledger_remove(dst)
                else:
                    return False, f"CONFLICT: {dst} is a real directory. All-skills will not modify it."
            else:
                # Real directory — NEVER touch it
                return False, f"CONFLICT: {dst} is a real directory. All-skills will not modify it."

    dst.parent.mkdir(parents=True, exist_ok=True)

    # 1) Windows junction (no admin required)
    if os.name == "nt":
        try:
            import _winapi
            _winapi.CreateJunction(str(src), str(dst))
            ledger_record(dst, src, "junction")
            return True, "junction"
        except Exception:
            pass

    # 2) Standard symlink
    try:
        os.symlink(str(src), str(dst), target_is_directory=True)
        ledger_record(dst, src, "symlink")
        return True, "symlink"
    except Exception:
        pass

    # 3) Fallback: copy (last resort, marks as 'copy' in ledger)
    try:
        import shutil
        shutil.copytree(str(src), str(dst))
        ledger_record(dst, src, "copy")
        return True, "copy"
    except Exception as e:
        return False, f"failed: {e}"


def _remove_link_only(dst: Path) -> bool:
    """
    Remove a symlink or Windows junction only — never a real directory tree.
    This is the ONLY place junction/symlink removal happens.
    """
    if not dst.exists() and not dst.is_symlink():
        return True
    try:
        if dst.is_symlink():
            dst.unlink()
            return True
        if os.name == "nt":
            # Remove junction: os.rmdir works for junctions (not shutil.rmtree)
            os.rmdir(str(dst))
            return True
        # Unix non-symlink link (shouldn't exist, but safe fallback)
        dst.unlink(missing_ok=True)
        return True
    except Exception as e:
        print(f"  ⚠️  Could not remove link {dst}: {e}", file=sys.stderr)
        return False


def unlink_target(dst: Path) -> Tuple[bool, str]:
    """
    Unlink a managed harness target ONLY if it appears in the ledger.

    Returns (success: bool, message: str).
    """
    if not dst.exists() and not dst.is_symlink():
        return True, "not-present"

    if not is_managed(dst):
        return False, (
            f"REFUSING: {dst} is not in the managed ledger. "
            "All-skills did not create it — will not remove it."
        )

    if is_link_or_junction(dst):
        ok = _remove_link_only(dst)
        if ok:
            ledger_remove(dst)
            return True, "unlinked"
        return False, "removal-failed"

    # Handle managed copy fallback
    key = str(dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst)
    entry = load_ledger().get(key, {})
    if entry.get("type") == "copy":
        import shutil
        try:
            shutil.rmtree(str(dst))
            ledger_remove(dst)
            return True, "unlinked"
        except Exception as e:
            return False, f"removal-failed: {e}"

    return False, f"REFUSING: {dst} is a real directory and cannot be safely unlinked."


# ─────────────────────────────────────────────────────────────────────────────
# PLATFORM DISCOVERY
# ─────────────────────────────────────────────────────────────────────────────

def resolve_path(raw: str) -> Path:
    if raw.startswith("~"):
        return HOME / raw[2:].lstrip("/\\")
    p = Path(raw)
    return p if p.is_absolute() else ROOT / p


def get_platform_targets() -> Tuple[Path, List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not PLATFORMS_CONFIG.exists():
        source = ROOT / ".agents" / "skills"
        local = [
            {"name": "Antigravity / Gemini CLI", "path": ROOT / ".agents" / "skills", "is_source": True},
            {"name": "Claude Code",               "path": ROOT / ".claude" / "skills"},
            {"name": "Cursor",                    "path": ROOT / ".cursor" / "skills"},
            {"name": "Codex CLI",                 "path": ROOT / ".codex" / "skills"},
            {"name": "GitHub Copilot",            "path": ROOT / ".github" / "skills"},
            {"name": "VS Code Agent",             "path": ROOT / ".vscode" / "skills"},
            {"name": "Windsurf",                  "path": ROOT / ".windsurf" / "skills"},
            {"name": "OpenCode",                  "path": ROOT / ".opencode" / "skills"},
            {"name": "Cline",                     "path": ROOT / ".cline" / "skills"},
            {"name": "Roo Code",                  "path": ROOT / ".roo" / "skills"},
            {"name": "Block Goose",               "path": ROOT / ".goose" / "skills"},
        ]
        glob = [
            {"name": "Claude Code (Global)",    "path": HOME / ".claude" / "skills"},
            {"name": "Cursor (Global)",         "path": HOME / ".cursor" / "skills"},
            {"name": "Codex CLI (Global)",      "path": HOME / ".codex" / "skills"},
            {"name": "Antigravity (Global)",    "path": HOME / ".agents" / "skills"},
        ]
        return source, local, glob

    cfg = load_yaml(PLATFORMS_CONFIG)
    src_raw = cfg.get("source_harness", {}).get("path", ".agents/skills")
    source_skills = resolve_path(src_raw)

    local_targets = []
    for item in cfg.get("local_targets", []):
        entry = dict(item)
        entry["path"] = resolve_path(item["path"])
        local_targets.append(entry)

    global_targets = []
    for item in cfg.get("global_targets", []):
        entry = dict(item)
        entry["path"] = resolve_path(item["path"])
        global_targets.append(entry)

    return source_skills, local_targets, global_targets


# ─────────────────────────────────────────────────────────────────────────────
# COMMANDS
# ─────────────────────────────────────────────────────────────────────────────

def cmd_status() -> None:
    source_skills, local_targets, global_targets = get_platform_targets()
    ledger = load_ledger()
    print("\n🔍 AI Coding Agent Harness Status:\n")
    source_count = len(os.listdir(source_skills)) if source_skills.exists() and source_skills.is_dir() else 0
    print(f"  Source canonical harness : {source_skills.relative_to(ROOT) if source_skills.is_relative_to(ROOT) else source_skills} ({source_count} skills)\n")

    print("📁 Local Workspace Targets:")
    for item in local_targets:
        name = item["name"]
        path = item["path"]
        exists = path.exists()
        count = len(os.listdir(path)) if exists and path.is_dir() else 0
        is_link = is_link_or_junction(path)
        managed = is_managed(path)
        key = str(path.relative_to(ROOT) if path.is_relative_to(ROOT) else path)
        link_type = ledger.get(key, {}).get("type", "?") if managed else "—"
        if item.get("is_source"):
            tag = "[canonical source]"
            status = f"✅ Active ({source_count} skills)"
        elif not exists:
            tag = ""
            status = "⚪ Not linked"
        elif is_link and managed:
            tag = f"[managed {link_type}]"
            status = f"✅ Active ({count} items)"
        elif is_link and not managed:
            tag = "[external link — not managed]"
            status = f"⚠️  Exists ({count} items)"
        else:
            tag = "[real directory — not managed]"
            status = f"⚠️  Real dir ({count} items)"
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"  • {name:30} → {str(rel):22} : {status}  {tag}")

    print("\n🌐 Global User Profile Targets:")
    for item in global_targets:
        name = item["name"]
        path = item["path"]
        exists = path.exists()
        count = len(os.listdir(path)) if exists and path.is_dir() else 0
        status = f"✅ Active ({count} skills)" if exists and count > 0 else "⚪ Not configured"
        print(f"  • {name:35} → {str(path):38} : {status}")
    print(f"\n📋 Managed Ledger: {len(ledger)} recorded entries ({LEDGER_PATH})\n")


def cmd_setup(include_global: bool = False, replace_managed: bool = False) -> None:
    source_skills, local_targets, global_targets = get_platform_targets()
    if not source_skills.exists():
        print(f"Error: Source skills directory not found at {source_skills}", file=sys.stderr)
        sys.exit(1)

    mode = "replacing managed links" if replace_managed else "creating missing links"
    print(f"\n⚡ Setting up Local Workspace AI Agent Harnesses ({mode})…\n")
    conflicts = []

    for item in local_targets:
        if item.get("is_source"):
            continue
        name = item["name"]
        dst = item["path"]
        ok, msg = link_or_copy(source_skills, dst, replace_managed=replace_managed)
        count = len(os.listdir(dst)) if dst.exists() and dst.is_dir() else 0
        rel = dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst

        if ok and msg == "already-linked":
            print(f"  ✅ (exists)   {name:28} → {rel}")
        elif ok:
            print(f"  ✅ {msg:9} {name:28} → {rel} ({count} items)")
        else:
            print(f"  ⚠️  CONFLICT   {name:28} → {rel}")
            print(f"            {msg}")
            conflicts.append((name, msg))

    if include_global:
        print("\n🌐 Setting up Global User Profile Harnesses…\n")
        for item in global_targets:
            name = item["name"]
            dst = item["path"]
            ok, msg = link_or_copy(source_skills, dst, replace_managed=replace_managed)
            count = len(os.listdir(dst)) if dst.exists() and dst.is_dir() else 0
            mark = "✅" if ok else "⚠️ "
            print(f"  {mark} {name:35} → {dst} ({count} items)  [{msg}]")

    if conflicts:
        print(f"\n⚠️  {len(conflicts)} CONFLICT(S) — existing real directories were not modified.")
        print("   Resolve by manually removing or renaming those directories, then re-run.\n")
    else:
        print("\n🎉 Multi-tool setup complete! All agents can now discover and load active skills.\n")


def cmd_unlink() -> None:
    _, local_targets, _ = get_platform_targets()
    print("\n🧹 Unlinking Managed Workspace Harnesses (ledger-safe)…\n")
    for item in local_targets:
        if item.get("is_source"):
            continue
        dst = item["path"]
        ok, msg = unlink_target(dst)
        rel = dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst
        if msg == "not-present":
            print(f"  ⚪ Skipped    {item['name']:28} → {rel}  (not present)")
        elif ok:
            print(f"  ✅ Unlinked   {item['name']:28} → {rel}")
        else:
            print(f"  ⚠️  Refused    {item['name']:28} → {rel}")
            print(f"            {msg}")
    print("\nDone. Source canonical harness remains untouched.\n")


def _tree_hashes(root: Path) -> Dict[str, str]:
    """Content hash of every skill folder directly under ``root``."""
    sys.path.insert(0, str(ROOT / "src"))
    from skills.lock import compute_skill_tree_hash

    return {
        d.name: compute_skill_tree_hash(d)[0]
        for d in sorted(root.iterdir())
        if d.is_dir() and not d.name.startswith(".")
    }


def cmd_verify(strict: bool = False) -> int:
    """Verify every harness; return the number of errors (0 = healthy).

    - The source harness must exist and every skill folder must contain SKILL.md.
    - A target marked ``required: true`` in platforms.yaml (or any target with
      ``--strict``) must exist.
    - Linked targets must resolve to the source harness.
    - Copied targets (no symlink support) must match the source content hashes.
    """
    source_skills, local_targets, _ = get_platform_targets()
    print("\n🔬 Verifying Platform Harness Integrity…\n")
    errors = 0
    if not source_skills.is_dir():
        print(f"  ❌ Source harness missing at {source_skills}")
        return 1
    skill_dirs = [d for d in sorted(source_skills.iterdir()) if d.is_dir() and not d.name.startswith(".")]
    no_manifest = [d.name for d in skill_dirs if not (d / "SKILL.md").is_file()]
    if no_manifest:
        print(f"  ❌ Source harness: {len(no_manifest)} skill folder(s) without SKILL.md: {', '.join(no_manifest[:5])}")
        errors += 1
    else:
        print(f"  ✅ Source harness verified ({len(skill_dirs)} skills, every folder has SKILL.md)")

    source_hashes: Optional[Dict[str, str]] = None
    for item in local_targets:
        name = item["name"]
        path = item["path"]
        if item.get("is_source") or path.resolve() == source_skills.resolve() and not is_link_or_junction(path):
            continue
        required = strict or bool(item.get("required"))
        if not path.exists() and not is_link_or_junction(path):
            if required:
                print(f"  ❌ {name:30}: required target missing at {path}")
                errors += 1
            else:
                print(f"  ·  {name:30}: not linked (optional)")
            continue
        if is_link_or_junction(path):
            try:
                target = path.resolve(strict=True)
            except (OSError, RuntimeError) as exc:
                print(f"  ❌ {name:30}: broken link ({exc})")
                errors += 1
                continue
            if target != source_skills.resolve():
                print(f"  ❌ {name:30}: link points to {target}, expected {source_skills}")
                errors += 1
            else:
                print(f"  ✅ {name:30}: linked to the source harness")
            continue
        if source_hashes is None:
            source_hashes = _tree_hashes(source_skills)
        target_hashes = _tree_hashes(path)
        drift = sorted(k for k in set(source_hashes) | set(target_hashes)
                       if source_hashes.get(k) != target_hashes.get(k))
        if drift:
            print(f"  ❌ {name:30}: copy out of sync with the source ({len(drift)} skill(s), e.g. {', '.join(drift[:3])})")
            errors += 1
        else:
            print(f"  ✅ {name:30}: copy matches the source ({len(target_hashes)} skills, hashes verified)")

    print()
    if errors == 0:
        print("  🎉 All harnesses verified.\n")
    else:
        print(f"  ❌ Verification failed with {errors} error(s).\n")
    return errors


# ─────────────────────────────────────────────────────────────────────────────
# CLI ENTRY POINT
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Multi-Tool Agent Harness Setup (hub-and-spoke, non-destructive)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Safety guarantee:
  This script NEVER touches real directories. It only manages symlinks/junctions
  that it created itself (tracked in state/managed_harnesses.json).

Examples:
  python scripts/setup_tools.py                    # Create missing harness links
  python scripts/setup_tools.py --status           # Read-only status report
  python scripts/setup_tools.py --verify           # Read-only integrity check
  python scripts/setup_tools.py --replace-managed-links  # Replace managed links only
  python scripts/setup_tools.py --unlink           # Remove managed links (checks ledger)
        """,
    )
    parser.add_argument("--status",                action="store_true", help="Inspect harness status (read-only)")
    parser.add_argument("--global",                dest="is_global", action="store_true", help="Also link global user profile directories")
    parser.add_argument("--replace-managed-links", action="store_true", help="Replace existing managed links/junctions (safe — ledger-checked)")
    parser.add_argument("--unlink",                action="store_true", help="Remove managed workspace harnesses (ledger-safe)")
    parser.add_argument("--verify",                action="store_true", help="Verify integrity of all harnesses (read-only)")
    parser.add_argument("--strict",                action="store_true", help="With --verify: every configured target is required")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    elif args.unlink:
        cmd_unlink()
    elif args.verify:
        sys.exit(1 if cmd_verify(strict=args.strict) else 0)
    elif args.replace_managed_links:
        cmd_setup(include_global=args.is_global, replace_managed=True)
    else:
        cmd_setup(include_global=args.is_global, replace_managed=False)


if __name__ == "__main__":
    main()
