"""Agent Skills Library — core router, registry, and loader."""
from .registry import Registry, SkillEntry, load_registry
from .router import Router, RouteBreakdown, RouteMatch
from .loader import Loader, load_skill, parse_frontmatter
from .validator import Validator, ValidationResult
from .dependencies import DependencyStatus, check_dependencies
from .updater import UpdateStatus, check_updates
from .quality import QualityReport, score_entry, score_all
from .lifecycle import (
    LIFECYCLE_STATES,
    can_transition,
    is_active,
    is_valid,
    transition,
)
from .chains import ChainResolver, ChainStore, SkillChain, load_chains
from .conflicts import ConflictRecord, ConflictStore, load_conflicts
from .security import Finding, scan_all, scan_skill, high_severity

__all__ = [
    "Registry",
    "SkillEntry",
    "load_registry",
    "Router",
    "RouteMatch",
    "RouteBreakdown",
    "Loader",
    "load_skill",
    "parse_frontmatter",
    "Validator",
    "ValidationResult",
    "DependencyStatus",
    "check_dependencies",
    "UpdateStatus",
    "check_updates",
    "QualityReport",
    "score_entry",
    "score_all",
    "LIFECYCLE_STATES",
    "can_transition",
    "is_active",
    "is_valid",
    "transition",
    "ChainResolver",
    "ChainStore",
    "SkillChain",
    "load_chains",
    "ConflictRecord",
    "ConflictStore",
    "load_conflicts",
    "Finding",
    "scan_all",
    "scan_skill",
    "high_severity",
]

__version__ = "1.2.0"