"""
Helper utilities for the skill system
"""

import time
import functools
import re
from typing import Callable, Any, Dict, List


def timed(func: Callable) -> Callable:
    """Decorator to measure execution time of functions"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"[{func.__name__}] executed in {elapsed:.4f}s")
        return result
    return wrapper


def format_slug(text: str) -> str:
    """Format string into a normalized skill slug"""
    slug = text.lower().strip()
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"[^a-z0-9\-.]", "", slug)
    return slug.strip("-")


def render_ascii_tree(tree: Dict[str, Any], indent: str = "") -> str:
    """Render a nested dependency dictionary into readable ASCII tree"""
    lines = []
    name = tree.get("name", "unknown")
    level = tree.get("level", "")
    lines.append(f"{indent}├── {name} ({level})")
    
    deps = tree.get("dependencies", {})
    sub_indent = indent + "│   "
    for dep_name, dep_tree in deps.items():
        if isinstance(dep_tree, dict):
            lines.append(render_ascii_tree(dep_tree, sub_indent))
        else:
            lines.append(f"{sub_indent}├── {dep_name}")
    return "\n".join(lines)
