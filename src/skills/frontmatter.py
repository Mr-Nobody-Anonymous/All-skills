"""YAML frontmatter parsing without external dependencies.

A minimal, dependency-free YAML-ish frontmatter parser tailored for SKILL.md files.
It supports the subset we actually use:

- ``key: value``
- ``key: [item1, item2]`` (inline list; ``key: []`` for an empty list)
- ``key:`` followed by an indented block of ``- item`` lines (block list)
- arbitrarily nested indented mappings (e.g. ``permissions``, ``compatibility``,
  or the ``metadata`` blocks used by some imported skills)

Scalars are intentionally left as strings (matching the historical behavior of
this module) so downstream coercion helpers keep working unchanged. Multi-line
values are not supported.
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
    entries = _tokenize(raw_meta)
    if not entries:
        return {}, body
    root_indent = entries[0][0]
    # Rebase so the first line is treated as the root level.
    if root_indent != 0:
        entries = [(ind - root_indent, text) for ind, text in entries]
    block, _ = _parse_block(entries, 0, 0)
    if not isinstance(block, dict):
        return {}, body
    return block, body


def _tokenize(raw: str) -> List[Tuple[int, str]]:
    """Convert raw frontmatter lines into (indent, text) tuples, blanks removed."""
    entries: List[Tuple[int, str]] = []
    for line in raw.splitlines():
        if not line.strip():
            continue
        stripped = line.lstrip(" ")
        indent = len(line) - len(stripped)
        entries.append((indent, stripped.rstrip()))
    return entries


def _parse_block(entries: List[Tuple[int, str]], i: int, indent: int) -> Tuple[Dict[str, Any], int]:
    """Parse a mapping block at ``indent`` starting at ``entries[i]``.

    Returns (mapping, next_index).
    """
    result: Dict[str, Any] = {}
    n = len(entries)
    while i < n:
        cur, text = entries[i]
        if cur < indent:
            break
        if cur > indent:
            # A deeper block appeared without an owning key — stop here so the
            # caller handles it; this mirrors tolerant behavior rather than crash.
            break
        if text.startswith("- "):
            # Unexpected list item at mapping level; skip defensively.
            i += 1
            continue
        key, sep, raw_value = text.partition(":")
        key = key.strip()
        if not sep:
            # Malformed line (no colon) — keep going like the old parser.
            i += 1
            continue
        value = raw_value.strip()
        if value == "":
            if i + 1 < n and entries[i + 1][0] > indent:
                child_indent = entries[i + 1][0]
                if entries[i + 1][1].startswith("- "):
                    child, i = _parse_list(entries, i + 1, child_indent)
                else:
                    child, i = _parse_block(entries, i + 1, child_indent)
                result[key] = child
            else:
                # Empty key with no children — preserve historical "empty list".
                result[key] = []
                i += 1
        else:
            result[key] = _parse_value(value)
            i += 1
    return result, i


def _parse_list(entries: List[Tuple[int, str]], i: int, indent: int) -> Tuple[List[Any], int]:
    """Parse a block list at ``indent`` starting at ``entries[i]``.

    Returns (list, next_index).
    """
    result: List[Any] = []
    n = len(entries)
    while i < n:
        cur, text = entries[i]
        if cur < indent:
            break
        if cur > indent:
            # Nested children of a list item are not supported at this level.
            i += 1
            continue
        if not text.startswith("- "):
            break
        item = text[2:].strip()
        if ":" in item:
            # Inline mapping item: "- key: value" -> {key: value}
            sub_key, _, sub_raw = item.partition(":")
            sub_value = sub_raw.strip()
            result.append({sub_key.strip(): _parse_value(sub_value) if sub_value else []})
        else:
            result.append(_strip_quotes(item))
        i += 1
    return result, i


def _parse_value(value: str) -> Any:
    """Parse a single scalar or inline list value."""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        items: List[str] = []
        if inner:
            for piece in _split_list(inner):
                items.append(_strip_quotes(piece))
        return items
    return _strip_quotes(value)


def _strip_quotes(s: str) -> str:
    s = s.strip()
    if len(s) >= 2 and ((s[0] == s[-1] == '"') or (s[0] == s[-1] == "'")):
        return s[1:-1]
    return s


def _split_list(s: str) -> List[str]:
    # Naive comma split — good enough for our frontmatter subset.
    return [piece.strip() for piece in s.split(",") if piece.strip()]


def dump_frontmatter(meta: Dict[str, Any]) -> str:
    """Serialize a dict back to YAML-ish frontmatter (mappings, lists, scalars)."""
    lines = ["---"]
    for k, v in meta.items():
        _dump_value(lines, k, v, 0)
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def _dump_value(lines: List[str], key: str, value: Any, indent: int) -> None:
    """Serialize a single frontmatter value at a given indentation."""
    pad = "  " * indent
    if isinstance(value, dict):
        if not value:
            lines.append(f"{pad}{key}: {{}}")
            return
        lines.append(f"{pad}{key}:")
        for k, v in value.items():
            _dump_value(lines, k, v, indent + 1)
    elif isinstance(value, list):
        if not value:
            lines.append(f"{pad}{key}: []")
        elif all(len(str(x)) < 60 for x in value) and len(value) <= 5:
            joined = ", ".join(_quote_if_needed(str(x)) for x in value)
            lines.append(f"{pad}{key}: [{joined}]")
        else:
            lines.append(f"{pad}{key}:")
            for x in value:
                lines.append(f"{pad}  - {_quote_if_needed(str(x))}")
    else:
        lines.append(f"{pad}{key}: {_quote_if_needed(str(value))}")


def _quote_if_needed(s: str) -> str:
    if any(c in s for c in [":", "#", "&", "*", "{", "}", "[", "]"]):
        return f'"{s}"'
    return s