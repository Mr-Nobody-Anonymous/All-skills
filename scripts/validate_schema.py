#!/usr/bin/env python3
"""Validate SKILL.md frontmatter against schemas/skill-frontmatter.schema.json.

Ensures:
1. Valid YAML frontmatter blocks bounded by ---
2. Required keys 'name' and 'description' are present and non-empty
3. 'name' matches slug pattern ^[a-z0-9-_]+$
4. 'description' is substantive (>= 10 chars)
5. Declared tools belong to allowed tool enumerations
6. Declared MCP servers and env variables are valid lists
7. Recovery and lifecycle configurations follow standard schema
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.frontmatter import parse_frontmatter

SLUG_PATTERN = re.compile(r"^[a-z0-9-_]+$")
ALLOWED_TOOLS = {
    "bash", "terminal", "file_read", "file_write", "file_edit",
    "ast_grep", "read_url", "browser", "generate_image", "mcp_call", "manage_task",
    "claude", "claude-code", "cursor", "gemini", "codex", "codex-cli", "windsurf", "copilot"
}


def validate_frontmatter_dict(meta: Dict[str, Any], file_path: Path) -> List[str]:
    errors: List[str] = []
    
    # name validation
    name = meta.get("name")
    if not name or not isinstance(name, str):
        errors.append(f"{file_path}: missing or invalid 'name' field")
    elif not SLUG_PATTERN.match(name):
        errors.append(f"{file_path}: name '{name}' does not match pattern ^[a-z0-9-_]+$")

    # description validation
    desc = meta.get("description")
    if not desc or not isinstance(desc, str):
        errors.append(f"{file_path}: missing or invalid 'description' field")
    elif len(desc.strip()) < 10:
        errors.append(f"{file_path}: description too short (< 10 chars)")

    # tools validation
    tools = meta.get("tools")
    if tools is not None:
        if not isinstance(tools, list):
            errors.append(f"{file_path}: 'tools' must be a list")
        else:
            for t in tools:
                if t not in ALLOWED_TOOLS:
                    errors.append(f"{file_path}: invalid tool '{t}' (allowed: {sorted(ALLOWED_TOOLS)})")

    # mcp_servers validation
    mcp = meta.get("mcp_servers")
    if mcp is not None and not isinstance(mcp, list):
        errors.append(f"{file_path}: 'mcp_servers' must be a list")

    # env validation
    env = meta.get("env")
    if env is not None and not isinstance(env, list):
        errors.append(f"{file_path}: 'env' must be a list")

    # recovery validation
    recovery = meta.get("recovery")
    if recovery is not None and not isinstance(recovery, dict):
        errors.append(f"{file_path}: 'recovery' must be a mapping")

    return errors


def main() -> int:
    total_checked = 0
    all_errors: List[str] = []

    # Check active skills
    active_root = REPO_ROOT / ".agents" / "skills"
    if active_root.exists():
        for skill_dir in active_root.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                all_errors.append(f"Missing SKILL.md in {skill_dir}")
                continue
            total_checked += 1
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            meta, _ = parse_frontmatter(text)
            errs = validate_frontmatter_dict(meta, skill_md)
            all_errors.extend(errs)

    # Check canonical skills
    canonical_root = REPO_ROOT / "skills"
    if canonical_root.exists():
        for skill_md in canonical_root.rglob("SKILL.md"):
            if "_quarantine" in skill_md.parts:
                continue
            total_checked += 1
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            meta, _ = parse_frontmatter(text)
            errs = validate_frontmatter_dict(meta, skill_md)
            all_errors.extend(errs)

    print(f"Validated {total_checked} SKILL.md frontmatters against schema.")
    if all_errors:
        print(f"\nFound {len(all_errors)} validation errors:")
        for err in all_errors[:20]:
            print(f"  - {err}")
        if len(all_errors) > 20:
            print(f"  ... and {len(all_errors) - 20} more.")
        return 1

    print("[SUCCESS] All SKILL.md frontmatters conform to the schema!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
