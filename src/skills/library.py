"""Convenience helpers for quick programmatic access."""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .registry import Registry, SkillEntry, load_registry
from .router import Router, RouteMatch


def discover(workspace_root: Path | None = None) -> Registry:
    return load_registry(workspace_root)


def route(query: str, workspace_root: Path | None = None, top_k: int = 1) -> List[RouteMatch]:
    reg = load_registry(workspace_root)
    return Router(reg).route(query, top_k=top_k)


def route_chain(query: str, workspace_root: Path | None = None, top_k: int = 5) -> List[RouteMatch]:
    reg = load_registry(workspace_root)
    return Router(reg).route_chain(query, top_k=top_k)


def load(skill_id: str, workspace_root: Path | None = None):
    root = workspace_root or Path.cwd()
    from .loader import load_skill
    return load_skill(root / "skills", skill_id)