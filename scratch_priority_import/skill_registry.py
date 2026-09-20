"""
Central Skill Registry with Comprehensive Metadata.
Supports Priority Tiers, Hardware Requirements, Platform Constraints,
Conflict Definitions, API Keys, and Locale Coverage.
"""

from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
import logging

from .registry import SkillRegistry as BaseSkillRegistry, SkillModule as BaseSkillModule, SkillDomain, SkillLevel
from .priority_levels import PriorityTier, get_tier_for_skill, get_tier_priority

logger = logging.getLogger(__name__)


@dataclass
class SkillMetadata:
    """Comprehensive metadata descriptor for voice and agent skills."""
    name: str
    category: str = "general"
    priority_tier: PriorityTier = PriorityTier.TIER_4_STANDARD
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    supported_platforms: List[str] = field(default_factory=lambda: ["linux", "windows", "darwin"])
    required_apis: List[str] = field(default_factory=list)
    memory_footprint_mb: float = 25.0
    locale_support: List[str] = field(default_factory=lambda: ["en-us"])
    intents: List[str] = field(default_factory=list)
    author: str = "All-Skills Platform"
    repository: str = ""
    description: str = ""
    enabled: bool = True
    loaded: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "priority_tier": self.priority_tier.label,
            "priority_level": int(self.priority_tier),
            "version": self.version,
            "dependencies": self.dependencies,
            "conflicts": self.conflicts,
            "supported_platforms": self.supported_platforms,
            "required_apis": self.required_apis,
            "memory_footprint_mb": self.memory_footprint_mb,
            "locale_support": self.locale_support,
            "intents": self.intents,
            "author": self.author,
            "repository": self.repository,
            "description": self.description,
            "enabled": self.enabled,
            "loaded": self.loaded,
        }


# Unified registry
EnhancedSkillRegistry = BaseSkillRegistry
SkillRegistry = BaseSkillRegistry

