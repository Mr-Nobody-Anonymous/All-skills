"""
Core Skill Manager.
Central coordinator for skill lifecycle (registration, load, start, shutdown, health).
"""

from typing import Dict, List, Optional, Any
import logging
from pathlib import Path

from scratch_priority_import.skill_registry import SkillRegistry, SkillMetadata
from scratch_priority_import.import_manager import ImportManager
from scratch_priority_import.priority_levels import PriorityTier

logger = logging.getLogger(__name__)


class SkillManager:
    """Manages active skills across all categories and tiers."""

    def __init__(self, skills_dir: str = "skills"):
        self.skills_dir = Path(skills_dir)
        self.registry = SkillRegistry()
        self.import_manager = ImportManager(self.registry)
        self._active_skills: Dict[str, Any] = {}

    def initialize(self) -> Dict[str, Any]:
        """Bootstrap the skill subsystem and load prioritized skills."""
        logger.info("Initializing All-Skills SkillManager...")
        res = self.import_manager.load_all()
        logger.info(f"SkillManager initialized: {res['loaded_count']} skills active")
        return res

    def get_skill(self, name: str) -> Optional[Any]:
        """Retrieve an active skill by name."""
        return self._active_skills.get(name) or self.import_manager.lazy_manager.get(name)

    def reload_skill(self, name: str) -> bool:
        """Reload a specific skill dynamically."""
        return self.import_manager.hot_load(name)

    def disable_skill(self, name: str) -> bool:
        """Disable and unload a skill."""
        return self.import_manager.unload(name)

    def list_skills(self) -> List[Dict[str, Any]]:
        """List summary of all registered skills and their operational status."""
        return [meta.to_dict() for meta in self.registry.get_all_metadata()]
