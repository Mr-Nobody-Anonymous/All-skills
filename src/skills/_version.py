"""Single authoritative source of truth for all-skills platform version."""
from __future__ import annotations
from pathlib import Path


def _resolve_version() -> str:
    p = Path(__file__).resolve()
    for parent in (p.parents[2], p.parents[1], p.parent):
        vfile = parent / "VERSION"
        if vfile.exists():
            try:
                v = vfile.read_text(encoding="utf-8").strip()
                if v:
                    return v
            except Exception:
                pass
    return "3.0.0"


__version__ = _resolve_version()
__version_info__ = tuple(int(part) for part in __version__.split(".") if part.isdigit())
