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

Usage:
    python scripts/setup_tools.py                # Set up local workspace harnesses
    python scripts/setup_tools.py --status       # Check health & detection across all tools
    python scripts/setup_tools.py --global       # Also link/sync to user profile directories
    python scripts/setup_tools.py --repair       # Repair broken links and refresh targets
    python scripts/setup_tools.py --update       # Update existing links/copies
    python scripts/setup_tools.py --unlink       # Unlink harnesses cleanly without deleting source
    python scripts/setup_tools.py --verify       # Verify resolve and manifest integrity
"""
from __future__ import annotations

import argparse
import os
import shutil
import sys
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
HOME = Path.home()

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
            {"name": "Claude Code", "path": ROOT / ".claude" / "skills"},
            {"name": "Cursor", "path": ROOT / ".cursor" / "skills"},
            {"name": "Codex CLI", "path": ROOT / ".codex" / "skills"},
        ]
        glob = [
            {"name": "Claude Code (User Global)", "path": HOME / ".claude" / "skills"},
            {"name": "Cursor (User Global)", "path": HOME / ".cursor" / "skills"},
            {"name": "Codex CLI (User Global)", "path": HOME / ".codex" / "skills"},
            {"name": "Antigravity / Agents (User Global)", "path": HOME / ".agents" / "skills"},
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

def link_or_copy(src: Path, dst: Path, force: bool = False) -> bool:
    if dst.exists():
        if force:
            unlink_target(dst)
        else:
            return True

    dst.parent.mkdir(parents=True, exist_ok=True)

    # Windows junction first (does not require admin privileges)
    if os.name == "nt":
        try:
            import _winapi
            _winapi.CreateJunction(str(src), str(dst))
            return True
        except Exception:
            pass

    # Try standard symlink
    try:
        os.symlink(str(src), str(dst), target_is_directory=True)
        return True
    except Exception:
        pass

    # Fallback: copy directory tree
    try:
        shutil.copytree(src, dst)
        return True
    except Exception as e:
        print(f"Failed to link or copy {src} -> {dst}: {e}", file=sys.stderr)
        return False

def unlink_target(dst: Path) -> bool:
    if not dst.exists() and not dst.is_symlink():
        return True
    try:
        if dst.is_symlink():
            dst.unlink()
            return True
        elif os.name == "nt":
            # Check for junction
            try:
                import _winapi
                # Removing junction directory on Windows
                os.rmdir(str(dst))
                return True
            except Exception:
                pass
        if dst.is_dir():
            shutil.rmtree(dst)
        else:
            dst.unlink()
        return True
    except Exception as e:
        print(f"Failed to unlink {dst}: {e}", file=sys.stderr)
        return False

def cmd_status() -> None:
    source_skills, local_targets, global_targets = get_platform_targets()
    print("\n🔍 AI Coding Agent Harness Status:\n")
    source_count = len(os.listdir(source_skills)) if source_skills.exists() and source_skills.is_dir() else 0
    print(f"Source canonical harness: {source_skills.relative_to(ROOT) if source_skills.is_relative_to(ROOT) else source_skills} ({source_count} skills)\n")

    print("📁 Local Workspace Targets:")
    for item in local_targets:
        name = item["name"]
        path = item["path"]
        exists = path.exists()
        count = len(os.listdir(path)) if exists and path.is_dir() else 0
        is_sym = path.is_symlink()
        tag = "[symlink/junction]" if is_sym else ("[source]" if item.get("is_source") else "[dir/copy]")
        status = f"✅ Active ({count} skills) {tag}" if exists and count > 0 else "❌ Not linked"
        rel = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
        print(f"  • {name:30} -> {str(rel):22} : {status}")

    print("\n🌐 Global User Profile Targets:")
    for item in global_targets:
        name = item["name"]
        path = item["path"]
        exists = path.exists()
        count = len(os.listdir(path)) if exists and path.is_dir() else 0
        status = f"✅ Active ({count} skills)" if exists and count > 0 else "⚪ Not configured"
        print(f"  • {name:35} -> {str(path):38} : {status}")
    print()

def cmd_setup(include_global: bool = False, force: bool = False) -> None:
    source_skills, local_targets, global_targets = get_platform_targets()
    if not source_skills.exists():
        print(f"Error: Source skills directory not found at {source_skills}", file=sys.stderr)
        sys.exit(1)

    print("\n⚡ Setting up Local Workspace AI Agent Harnesses...\n")
    for item in local_targets:
        if item.get("is_source"):
            continue
        name = item["name"]
        dst = item["path"]
        success = link_or_copy(source_skills, dst, force=force)
        count = len(os.listdir(dst)) if dst.exists() and dst.is_dir() else 0
        mark = "✅ Linked" if success else "❌ Failed"
        rel = dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst
        print(f"  {mark:10} {name:28} -> {rel} ({count} skills)")

    if include_global:
        print("\n🌐 Setting up Global User Profile Harnesses...\n")
        for item in global_targets:
            name = item["name"]
            dst = item["path"]
            success = link_or_copy(source_skills, dst, force=force)
            count = len(os.listdir(dst)) if dst.exists() and dst.is_dir() else 0
            mark = "✅ Linked" if success else "❌ Failed"
            print(f"  {mark:10} {name:35} -> {dst} ({count} skills)")

    print("\n🎉 Multi-tool setup complete! All agents can now discover and load active skills.\n")

def cmd_unlink() -> None:
    _, local_targets, _ = get_platform_targets()
    print("\n🧹 Unlinking Managed Workspace Harnesses...\n")
    for item in local_targets:
        if item.get("is_source"):
            continue
        dst = item["path"]
        if dst.exists() or dst.is_symlink():
            success = unlink_target(dst)
            mark = "✅ Unlinked" if success else "❌ Failed"
            rel = dst.relative_to(ROOT) if dst.is_relative_to(ROOT) else dst
            print(f"  {mark:12} {item['name']:28} -> {rel}")
        else:
            print(f"  ⚪ Skipped    {item['name']:28} (not present)")
    print("\nDone. Source canonical harness remains untouched.\n")

def cmd_verify() -> None:
    source_skills, local_targets, _ = get_platform_targets()
    print("\n🔬 Verifying Platform Harness Integrity...\n")
    errors = 0
    if not source_skills.exists():
        print(f"❌ Source harness missing at {source_skills}")
        errors += 1
    else:
        print(f"✅ Source canonical harness verified ({len(os.listdir(source_skills))} skills)")

    for item in local_targets:
        name = item["name"]
        path = item["path"]
        if not path.exists():
            continue
        skill_files = list(path.glob("*/SKILL.md"))
        if len(skill_files) == 0:
            print(f"⚠️  {name:28}: Target directory exists but no SKILL.md files found")
            errors += 1
        else:
            print(f"✅ {name:28}: Verified ({len(skill_files)} readable SKILL.md manifests)")

    if errors == 0:
        print("\n🎉 All active harnesses verified with 100% integrity!\n")
    else:
        print(f"\n⚠️  Verification completed with {errors} warnings/errors.\n")

def main() -> None:
    parser = argparse.ArgumentParser(description="Multi-Tool Agent Harness Setup")
    parser.add_argument("--status", action="store_true", help="Inspect status of tool harnesses")
    parser.add_argument("--global", dest="is_global", action="store_true", help="Also link to user home directories")
    parser.add_argument("--repair", action="store_true", help="Repair and refresh broken or stale harnesses")
    parser.add_argument("--update", action="store_true", help="Update all harness targets")
    parser.add_argument("--force", action="store_true", help="Force recreate links")
    parser.add_argument("--unlink", action="store_true", help="Unlink managed workspace harnesses")
    parser.add_argument("--verify", action="store_true", help="Verify integrity of all harnesses")
    args = parser.parse_args()

    if args.status:
        cmd_status()
    elif args.unlink:
        cmd_unlink()
    elif args.verify:
        cmd_verify()
    elif args.repair or args.update or args.force:
        cmd_setup(include_global=args.is_global, force=True)
    else:
        cmd_setup(include_global=args.is_global)

if __name__ == "__main__":
    main()
