#!/usr/bin/env python3
"""Enrich YAML frontmatter in SKILL.md files to meet SkillHub and multi-agent standards.

Adds missing fields:
- version: "1.0.0"
- author: "Mr-Nobody-Anonymous" (or preserves existing)
- tags: [list of relevant tags]
- compatibility: {claude-code: ">=1.0", skillhub: "*", cursor: ">=0.40", codex: "*"}
- risk: "low" (if not already set)
- network_access: false
- filesystem_access: "read"
- credential_access: false
- destructive_operations: false
"""
from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_COMPATIBILITY = {
    "claude-code": ">=1.0",
    "skillhub": "*",
    "cursor": ">=0.40",
    "codex": "*"
}

def derive_tags(name: str, meta: Dict[str, Any]) -> List[str]:
    tags: Set[str] = set()
    cat = meta.get("category")
    if cat:
        tags.add(str(cat).lower())
    domain = meta.get("domain")
    if domain:
        tags.add(str(domain).lower())
    # Add tokens from name
    for part in re.split(r"[-_]", name):
        if len(part) > 2 and part.isalpha():
            tags.add(part.lower())
    # Add keywords
    kws = meta.get("keywords") or []
    if isinstance(kws, list):
        for kw in kws[:4]:
            if isinstance(kw, str) and len(kw) > 2:
                tags.add(kw.lower())
    return sorted(list(tags))[:6]

def enrich_file(skill_md: Path) -> bool:
    try:
        content = skill_md.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {skill_md}: {e}")
        return False

    if not content.startswith("---"):
        return False

    parts = content.split("---", 2)
    if len(parts) < 3:
        return False

    try:
        meta = yaml.safe_load(parts[1]) or {}
    except Exception as e:
        print(f"Error parsing YAML in {skill_md}: {e}")
        return False

    modified = False

    # 1. version
    if "version" not in meta:
        meta["version"] = "1.0.0"
        modified = True

    # 2. author
    if "author" not in meta:
        meta["author"] = meta.get("original_author") or "Mr-Nobody-Anonymous"
        modified = True

    # 3. tags
    if "tags" not in meta or not meta["tags"]:
        meta["tags"] = derive_tags(meta.get("name", skill_md.parent.name), meta)
        modified = True

    # 4. compatibility
    if "compatibility" not in meta or not meta["compatibility"]:
        meta["compatibility"] = dict(DEFAULT_COMPATIBILITY)
        modified = True

    # 5. Security & sandbox scope defaults
    if "risk" not in meta:
        meta["risk"] = "low"
        modified = True
    if "network_access" not in meta:
        meta["network_access"] = False
        modified = True
    if "filesystem_access" not in meta:
        meta["filesystem_access"] = "read"
        modified = True
    if "credential_access" not in meta:
        meta["credential_access"] = False
        modified = True
    if "destructive_operations" not in meta:
        meta["destructive_operations"] = False
        modified = True

    if modified:
        # Re-dump YAML maintaining nice structure
        new_yaml = yaml.dump(meta, sort_keys=False, allow_unicode=True).strip()
        new_content = f"---\n{new_yaml}\n---" + parts[2]
        skill_md.write_text(new_content, encoding="utf-8")
        return True
    return False

def main() -> int:
    targets = [
        REPO_ROOT / ".agents" / "skills",
        REPO_ROOT / "skills"
    ]
    total_enriched = 0
    total_scanned = 0

    for target in targets:
        if not target.exists():
            continue
        for skill_md in target.rglob("SKILL.md"):
            if "_quarantine" in skill_md.parts:
                continue
            total_scanned += 1
            if enrich_file(skill_md):
                total_enriched += 1

    print(f"Scanned {total_scanned} SKILL.md files. Enriched {total_enriched} files with standard metadata.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
