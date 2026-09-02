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
