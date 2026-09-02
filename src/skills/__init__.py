"""Agent Skills Library — core router, registry, and loader."""
from .registry import Registry, SkillEntry, load_registry
from .router import Router, RouteMatch
from .loader import Loader, load_skill, parse_frontmatter
from .validator import Validator, ValidationResult
from .dependencies import DependencyStatus, check_dependencies
from .updater import UpdateStatus, check_updates

__all__ = [
    "Registry",
    "SkillEntry",
    "load_registry",
    "Router",
    "RouteMatch",
    "Loader",
    "load_skill",
    "parse_frontmatter",
    "Validator",
    "ValidationResult",
    "DependencyStatus",
    "check_dependencies",
    "UpdateStatus",
    "check_updates",
]

__version__ = "1.1.0"