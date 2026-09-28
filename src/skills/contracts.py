"""Per-skill execution contracts: declared permissions must match behaviour.

A skill's frontmatter declares what it may do (``filesystem_access``,
``network_access``, ``tools``) and its instructions say what the agent will
actually do. This module checks the two agree, so frontmatter presence is not
mistaken for correctness:

* write-capable tools (``file_write``, ``file_edit``, ...) require
  ``filesystem_access: write`` (or ``full``);
* instructions that direct the agent to change files — fix the code, apply a
  patch, add a regression test, edit or create a file, commit — require write
  access, unless the skill declares ``execution_mode: advisory`` (it only
  recommends changes for a human to make);
* network tools (``read_url``, ``browser``, ``web_search``, ...) require
  ``network_access: true``.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List

WRITE_TOOLS = {"file_write", "file_edit", "write_file", "edit_file", "generate_image"}
NETWORK_TOOLS = {"read_url", "browser", "web_search", "web_fetch", "mcp_call"}
WRITE_LEVELS = {"write", "full"}

# Imperative instructions that change the workspace. Deliberately specific:
# prose such as "a fix" or "tests exist" is not an instruction to modify files.
WRITE_INTENT = re.compile(
    r"(?im)^\s*(?:[-*]|\d+[.)])?\s*(?:\*\*)?"
    r"(?:fix|apply|patch|edit|modify|refactor|rewrite|implement|write|add|create|update|commit|delete|remove|rename)\b"
    r"[^\n]{0,80}\b(?:the\s+)?(?:code|file|files|fix|patch|bug|tests?|regression\s+tests?|function|module|implementation|changes?)\b"
)


@dataclass(frozen=True)
class ContractIssue:
    field: str
    message: str


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"true", "yes", "1", "on"}


def write_intent_lines(body: str, limit: int = 3) -> List[str]:
    """Instruction lines that direct the agent to modify the workspace."""
    in_fence = False
    hits: List[str] = []
    for line in body.splitlines():
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence and WRITE_INTENT.search(line):
            hits.append(line.strip()[:120])
            if len(hits) >= limit:
                break
    return hits


def check_contract(meta: Dict[str, Any], body: str) -> List[ContractIssue]:
    """Return the ways a skill's declared contract disagrees with its tools or instructions."""
    issues: List[ContractIssue] = []
    tools = {str(t).strip().lower() for t in (meta.get("tools") or [])} if isinstance(meta.get("tools"), list) else set()
    fs_access = str(meta.get("filesystem_access", "")).strip().lower()
    advisory = str(meta.get("execution_mode", "")).strip().lower() == "advisory"

    write_tools = sorted(tools & WRITE_TOOLS)
    if write_tools and fs_access not in WRITE_LEVELS:
        issues.append(ContractIssue(
            "filesystem_access",
            f"declares write tools {write_tools} but filesystem_access is {fs_access or 'unset'}",
        ))
    elif fs_access and fs_access not in WRITE_LEVELS and not advisory:
        evidence = write_intent_lines(body)
        if evidence:
            issues.append(ContractIssue(
                "filesystem_access",
                f"instructions modify files ({evidence[0]!r}) but filesystem_access is {fs_access}; "
                "declare filesystem_access: write, or execution_mode: advisory if the skill only recommends changes",
            ))
    network_tools = sorted(tools & NETWORK_TOOLS)
    if network_tools and "network_access" in meta and not _as_bool(meta.get("network_access")):
        issues.append(ContractIssue(
            "network_access", f"declares network tools {network_tools} but network_access is false",
        ))
    return issues
