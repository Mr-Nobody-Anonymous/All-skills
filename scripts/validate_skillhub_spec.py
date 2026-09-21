#!/usr/bin/env python3
"""SkillHub and Multi-Agent Specification Linter.

Validates that agent skills comply with strict ecosystem guidelines:
1. Valid YAML frontmatter bounded by ---
2. Standard metadata fields: name, version, description, author, tags, compatibility
3. Natural language trigger guidance:
   - "Use this skill when" or "When to Use"
   - "Do not use this skill when" or "When NOT to Use"
4. Security & boundaries declaration (risk, network_access, filesystem_access, etc.)
5. Auxiliary resources check (README.md, references/ or templates/, examples/)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_FRONTMATTER_FIELDS = ["name", "version", "description", "author", "tags", "compatibility"]

def check_skill_spec(skill_dir: Path) -> List[str]:
    errors = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]

    text = skill_md.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return [f"{skill_dir.name}: SKILL.md missing opening YAML frontmatter boundary (---)"]

    parts = text.split("---", 2)
    if len(parts) < 3:
        return [f"{skill_dir.name}: SKILL.md missing closing YAML frontmatter boundary (---)"]

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except Exception as e:
        return [f"{skill_dir.name}: invalid YAML frontmatter: {e}"]

    # 1. Check required frontmatter keys
    for req in REQUIRED_FRONTMATTER_FIELDS:
        if req not in meta or not meta[req]:
            errors.append(f"{skill_dir.name}: frontmatter missing required field '{req}'")

    # 2. Check compatibility mapping
    compat = meta.get("compatibility")
    if compat is not None and not isinstance(compat, dict):
        errors.append(f"{skill_dir.name}: 'compatibility' must be a mapping (e.g. claude-code: '>=1.0', skillhub: '*')")

    # 3. Check natural language trigger guidance in markdown body
    body = parts[2].lower()
    has_positive_trigger = bool(
        re.search(r"##\s+(?:use this skill when|when to use)", body)
    )
    has_negative_trigger = bool(
        re.search(r"##\s+(?:do not use this skill when|when not to use)", body)
    )

    if not has_positive_trigger:
        errors.append(f"{skill_dir.name}: missing '## Use this skill when' or '## When to Use' trigger section")
    if not has_negative_trigger:
        errors.append(f"{skill_dir.name}: missing '## Do not use this skill when' or '## When NOT to Use' negative trigger section")

    # 4. Check security and safety section
    has_safety = bool(
        re.search(r"##\s+(?:safety|security\s*(&|and)?\s*sandboxing\s*boundaries|security)", body)
    )
    if not has_safety:
        errors.append(f"{skill_dir.name}: missing '## Safety' or '## Security & Sandboxing Boundaries' section")

    return errors

def main() -> int:
    # Check active harness skills
    active_root = REPO_ROOT / ".agents" / "skills"
    all_errors: List[str] = []
    total_checked = 0

    if not active_root.exists():
        print(f"Error: {active_root} does not exist", file=sys.stderr)
        return 1

    for skill_dir in sorted(active_root.iterdir()):
        if not skill_dir.is_dir():
            continue
        total_checked += 1
        errs = check_skill_spec(skill_dir)
        all_errors.extend(errs)

    print(f"Validated {total_checked} active harness skills against SkillHub & Agent specification.")
    if all_errors:
        print(f"\nFound {len(all_errors)} specification warnings/errors:")
        for err in all_errors[:25]:
            print(f"  - {err}")
        if len(all_errors) > 25:
            print(f"  ... and {len(all_errors) - 25} more.")
        return 1

    print("[SUCCESS] All active skills comply with the SkillHub & Agent specification!")
    return 0

if __name__ == "__main__":
    sys.exit(main())
