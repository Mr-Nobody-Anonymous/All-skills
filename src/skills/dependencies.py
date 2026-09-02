"""Dependency checks for declared skill tools; never installs anything."""
from __future__ import annotations

import importlib.util
import shutil
from dataclasses import dataclass
from typing import Iterable, List

from .registry import SkillEntry


@dataclass(frozen=True)
class DependencyStatus:
    skill_id: str
    dependency: str
    available: bool
    optional: bool
    detail: str


def check_dependency(skill_id: str, declaration: str) -> DependencyStatus:
    optional = declaration.endswith("-optional") or declaration.startswith("optional:")
    name = declaration.removeprefix("optional:").removesuffix("-optional")
    alternatives = [part.strip() for part in name.split("-or-") if part.strip()]
    binary_aliases = {"gh-cli": "gh", "playwright": "playwright", "cypress": "cypress"}
    for candidate in alternatives:
        binary = binary_aliases.get(candidate, candidate)
        if shutil.which(binary):
            return DependencyStatus(skill_id, declaration, True, optional, f"command: {binary}")
        module = candidate.replace("-", "_")
        if importlib.util.find_spec(module) is not None:
            return DependencyStatus(skill_id, declaration, True, optional, f"python module: {module}")
    return DependencyStatus(skill_id, declaration, False, optional, "not detected")


def check_dependencies(entries: Iterable[SkillEntry]) -> List[DependencyStatus]:
    return [check_dependency(entry.id, dep) for entry in entries for dep in entry.dependencies]


# ---------------------------------------------------------------------------
# Structured dependency data (machine-readable form for skills/dependencies.json)
# ---------------------------------------------------------------------------

SYSTEM_BINARIES = {
    "git", "gh", "gh-cli", "node", "npm", "npx", "python", "python3", "pip",
    "docker", "docker-compose", "curl", "wget", "ffmpeg", "sqlite3", "psql",
    "mysql", "ruby", "go", "cargo", "rustc", "java", "make", "ffprobe",
}


def expand_declaration(declaration: str):
    """Split a dependency declaration into (canonical_name, optional, kind).

    ``kind`` is one of ``system`` (a binary/tool), ``python`` (an importable
    module), or ``api`` (an external service not detectible locally).
    Handles the ``optional:`` prefix, the ``-optional`` suffix, and ``-or-``
    alternatives (the primary alternative is used for the canonical name).
    """
    optional = declaration.endswith("-optional") or declaration.startswith("optional:")
    name = declaration.removeprefix("optional:").removesuffix("-optional")
    alternatives = [part.strip() for part in name.split("-or-") if part.strip()]
    primary = alternatives[0] if alternatives else name
    kind = "api"
    if any(a in SYSTEM_BINARIES for a in alternatives) or primary in SYSTEM_BINARIES:
        kind = "system"
    elif any(importlib.util.find_spec(a.replace("-", "_")) is not None for a in alternatives):
        kind = "python"
    return primary, optional, kind


def structured_dependency_status(entry: SkillEntry) -> dict:
    """Map a skill's flat dependency list to the structured form used by
    ``skills/dependencies.json``:

    {"required": [...], "optional": [...], "system": [...], "python": [...],
     "api": [...], "missing_required": [...], "missing_optional": [...]}
    """
    result = {
        "required": [], "optional": [], "system": [], "python": [], "api": [],
        "missing_required": [], "missing_optional": [],
    }
    for dep in entry.dependencies:
        status = check_dependency(entry.id, dep)
        canonical, optional, kind = expand_declaration(dep)
        bucket = "optional" if optional else "required"
        result[bucket].append(canonical)
        result[kind].append(canonical)
        if not status.available:
            result[f"missing_{bucket}"].append(canonical)
    # De-duplicate while preserving order.
    for key in list(result):
        seen: List[str] = []
        for item in result[key]:
            if item not in seen:
                seen.append(item)
        result[key] = seen
    return result


def generate_dependencies_json(entries: Iterable[SkillEntry]) -> dict:
    """Build the machine-readable dependencies index document."""
    return {
        "version": 1,
        "skills": {entry.id: structured_dependency_status(entry) for entry in entries},
    }


def dump_dependencies_json(entries: Iterable[SkillEntry], out_path: Path) -> None:
    """Write ``skills/dependencies.json`` from a set of skill entries."""
    import json

    data = generate_dependencies_json(entries)
    out_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
