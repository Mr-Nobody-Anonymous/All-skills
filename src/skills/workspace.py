"""Locate the All-Skills workspace a command operates on.

The same rule applies to every entry point (``all-skills``, ``allskills`` via
npm/npx, and the scripts in a checkout):

1. an explicit ``--workspace PATH``;
2. the ``ALL_SKILLS_WORKSPACE`` environment variable;
3. the nearest directory, starting at the current one, that contains
   ``skills/registry.json``;
4. the source checkout this package was installed from (editable installs).

A workspace is any directory with ``skills/registry.json``. The large
``awesome_skills/`` catalog is optional: commands that need catalog content
say so explicitly when it is not provisioned.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Optional, Union

ENV_VAR = "ALL_SKILLS_WORKSPACE"
MARKER = Path("skills") / "registry.json"


class WorkspaceNotFound(RuntimeError):
    """No All-Skills workspace could be located."""


def is_workspace(path: Path) -> bool:
    return (Path(path) / MARKER).is_file()


def catalog_provisioned(workspace: Path) -> bool:
    return (Path(workspace) / "awesome_skills").is_dir()


def resolve_workspace(explicit: Optional[Union[str, Path]] = None, cwd: Optional[Path] = None) -> Path:
    """Return the workspace root, or raise WorkspaceNotFound with guidance."""
    for label, raw in (("--workspace", explicit), (ENV_VAR, os.environ.get(ENV_VAR))):
        if raw:
            path = Path(raw).expanduser().resolve()
            if not is_workspace(path):
                raise WorkspaceNotFound(f"{label}={path} is not an All-Skills workspace (no {MARKER.as_posix()})")
            return path
    start = (cwd or Path.cwd()).resolve()
    for candidate in (start, *start.parents):
        if is_workspace(candidate):
            return candidate
    checkout = Path(__file__).resolve().parents[2]
    if is_workspace(checkout):
        return checkout
    raise WorkspaceNotFound(
        "No All-Skills workspace found. Run inside a clone of "
        "https://github.com/Mr-Nobody-Anonymous/All-skills, pass --workspace PATH, "
        f"or set {ENV_VAR}."
    )
