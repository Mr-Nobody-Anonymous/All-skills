#!/usr/bin/env python3
"""Generate the unified Agent Infrastructure Manifest (manifest.json).

Maps skills across the repository to:
- Tool permissions and capabilities (bash, file_read, file_edit, ast_grep, etc.)
- Model Context Protocol (MCP) server requirements
- Environment variables
- Activation triggers and keywords
- Pre- and Post-condition execution hooks
- Fallback and recovery policies
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.frontmatter import parse_frontmatter


def infer_tools_from_text(text: str) -> List[str]:
    """Infer tool permissions required based on keywords in the skill text."""
    tools: List[str] = ["file_read"]
    low = text.lower()
    if any(k in low for k in ["bash", "shell", "run command", "terminal", "powershell", "execute command"]):
        tools.append("bash")
    if any(k in low for k in ["edit file", "modify file", "write_to_file", "replace_file_content", "create file"]):
        tools.append("file_edit")
        tools.append("file_write")
    if any(k in low for k in ["ast", "tree-sitter", "ast-grep", "abstract syntax tree"]):
        tools.append("ast_grep")
    if any(k in low for k in ["browser", "playwright", "puppeteer", "selenium", "web page"]):
        tools.append("browser")
    if any(k in low for k in ["http", "fetch", "url", "curl", "api request"]):
        tools.append("read_url")
    return sorted(list(set(tools)))


def infer_mcp_from_tools(tools: List[str]) -> List[str]:
    """Map tool requirements to standard MCP servers."""
    mcp = ["filesystem"]
    if "read_url" in tools or "browser" in tools:
        mcp.append("fetch")
    if "bash" in tools:
        mcp.append("git")
    return sorted(list(set(mcp)))


def build_manifest() -> Dict[str, Any]:
    manifest: Dict[str, Any] = {
        "$schema": "./schemas/skill-frontmatter.schema.json",
        "schema_version": "1.1.0",
        "generated_at": "2026-09-20",
        "system_defaults": {
            "default_mcp_servers": ["filesystem", "git", "fetch", "memory"],
            "default_preconditions": ["check_environment", "check_git_clean"],
            "default_postconditions": ["verify_syntax"],
            "default_recovery": {
                "max_retries": 3,
                "loop_detection": True,
                "on_failure": "rollback"
            }
        },
        "skills": {}
    }

    # 1. Process Canonical Skills from skills/registry.json
    registry_file = REPO_ROOT / "skills" / "registry.json"
    if registry_file.exists():
        with open(registry_file, "r", encoding="utf-8") as f:
            registry_data = json.load(f)
        for entry in registry_data.get("skills", []):
            skill_id = entry.get("id")
            rel_path = entry.get("path")
            skill_md = REPO_ROOT / "skills" / rel_path / "SKILL.md"
            meta: Dict[str, Any] = {}
            body = ""
            if skill_md.exists():
                text = skill_md.read_text(encoding="utf-8", errors="replace")
                meta, body = parse_frontmatter(text)

            tools = meta.get("tools") or infer_tools_from_text(body or entry.get("description", ""))
            mcp = meta.get("mcp_servers") or infer_mcp_from_tools(tools)
            preconditions = meta.get("preconditions") or ["check_environment"]
            postconditions = meta.get("postconditions") or ["verify_syntax"]
            recovery = meta.get("recovery") or {
                "fallback_skill": entry.get("suggests_after", [None])[0] if entry.get("suggests_after") else None,
                "max_retries": 3,
                "on_failure": "rollback"
            }

            manifest["skills"][skill_id] = {
                "name": entry.get("name"),
                "category": entry.get("category"),
                "description": entry.get("description"),
                "version": entry.get("version", "1.0.0"),
                "path": f"skills/{rel_path}/SKILL.md",
                "harness_scope": "canonical",
                "triggers": entry.get("triggers", []),
                "aliases": entry.get("aliases", []),
                "keywords": entry.get("keywords", []),
                "tools": tools,
                "mcp_servers": mcp,
                "env": meta.get("env", []),
                "preconditions": preconditions,
                "postconditions": postconditions,
                "recovery": recovery
            }

    # 2. Process Active Harness Skills from .agents/skills/
    active_root = REPO_ROOT / ".agents" / "skills"
    if active_root.exists():
        for skill_dir in active_root.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue
            text = skill_md.read_text(encoding="utf-8", errors="replace")
            meta, body = parse_frontmatter(text)
            skill_id = f"active.{skill_dir.name}"
            tools = meta.get("tools") or infer_tools_from_text(body or meta.get("description", ""))
            mcp = meta.get("mcp_servers") or infer_mcp_from_tools(tools)

            manifest["skills"][skill_id] = {
                "name": meta.get("name", skill_dir.name),
                "category": meta.get("category", "workflow"),
                "description": meta.get("description", ""),
                "version": meta.get("version", "1.0.0"),
                "path": f".agents/skills/{skill_dir.name}/SKILL.md",
                "harness_scope": "active_harness",
                "triggers": meta.get("triggers", [skill_dir.name.replace("-", " ")]),
                "aliases": meta.get("aliases", [skill_dir.name]),
                "keywords": meta.get("keywords", skill_dir.name.split("-")),
                "tools": tools,
                "mcp_servers": mcp,
                "env": meta.get("env", []),
                "preconditions": meta.get("preconditions", ["check_environment"]),
                "postconditions": meta.get("postconditions", ["verify_syntax"]),
                "recovery": meta.get("recovery", {
                    "max_retries": 3,
                    "on_failure": "rollback"
                })
            }

    return manifest


def main() -> None:
    manifest = build_manifest()
    out_path = REPO_ROOT / "manifest.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)
    print(f"Generated manifest.json with {len(manifest['skills'])} indexed skills.")


if __name__ == "__main__":
    main()
