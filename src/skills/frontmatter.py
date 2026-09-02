"""YAML frontmatter parsing without external dependencies.

A minimal, dependency-free YAML-ish frontmatter parser tailored for SKILL.md files.
Supports the small subset we actually use:
- key: value
- key: [item1, item2]
- multi-line values are NOT supported (kept simple on purpose)
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Tuple


FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n(.*)$", re.DOTALL)


def parse_frontmatter(text: str) -> Tuple[Dict[str, Any], str]:
    """Split a SKILL.md into (frontmatter_dict, body_str).

    If no frontmatter is present, returns ({}, original_text).
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return {}, text
    raw_meta, body = m.group(1), m.group(2)
    meta: Dict[str, Any] = {}
    current_key: str | None = None
    current_list: List[str] | None = None
    for line in raw_meta.splitlines():
        if not line.strip():
            continue
        # List continuation
        if line.lstrip().startswith("- ") and current_list is not None:
            item = line.lstrip()[2:].strip()
            # strip surrounding quotes if present
            item = _strip_quotes(item)
            current_list.append(item)
            continue
        # New key
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            if value == "":
                # Possibly a list follows
                current_list = []
                meta[key] = current_list
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                items: List[str] = []
                if inner:
                    for piece in _split_list(inner):
                        items.append(_strip_quotes(piece))
                meta[key] = items
                current_list = None
                current_key = None
            else:
                meta[key] = _strip_quotes(value)
                current_list = None
                current_key = None
        else:
            # Malformed line — keep going
            continue
    return meta, body


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def _split_list(s: str) -> List[str]:
    # Naive comma split — good enough for our frontmatter subset.
    return [piece.strip() for piece in s.split(",") if piece.strip()]


def dump_frontmatter(meta: Dict[str, Any]) -> str:
    """Serialize a dict back to YAML-ish frontmatter."""
    lines = ["---"]
    for k, v in meta.items():
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                # Use inline form for short lists, block form for longer ones
                if all(len(str(x)) < 60 for x in v) and len(v) <= 5:
                    joined = ", ".join(_quote_if_needed(str(x)) for x in v)
                    lines.append(f"{k}: [{joined}]")
                else:
                    lines.append(f"{k}:")
                    for x in v:
                        lines.append(f"  - {_quote_if_needed(str(x))}")
        else:
            lines.append(f"{k}: {_quote_if_needed(str(v))}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def _quote_if_needed(s: str) -> str:
    if any(c in s for c in [":", "#", "&", "*", "{", "}", "[", "]"]):
        return f'"{s}"'
    return s