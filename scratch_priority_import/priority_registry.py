"""
Priority Registry for scratch_priority_import.
Registers skills with explicit priority rankings from 1 (Highest) to 100 (Lowest),
load strategies (eager vs lazy), and resource requirements.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field

@dataclass
class RegisteredSkill:
    name: str
    priority: int  # 1 to 100
    category: str = "general"
    dependencies: List[str] = field(default_factory=list)
    load_strategy: str = "eager"  # 'eager' or 'lazy'
    resource_requirements: Dict[str, Any] = field(default_factory=dict)
    enabled: bool = True
    supported_platforms: List[str] = field(default_factory=lambda: ["all"])

class PriorityRegistry:
    def __init__(self):
        self._skills: Dict[str, RegisteredSkill] = {}

    def register(self,
                 name: str,
                 priority: int,
                 category: str = "general",
                 dependencies: Optional[List[str]] = None,
                 load_strategy: str = "eager",
                 resource_requirements: Optional[Dict[str, Any]] = None,
                 enabled: bool = True,
                 supported_platforms: Optional[List[str]] = None) -> RegisteredSkill:
        """Registers a skill with priority rank 1-100."""
        clamped_priority = max(1, min(100, priority))
        skill = RegisteredSkill(
            name=name,
            priority=clamped_priority,
            category=category,
            dependencies=dependencies or [],
            load_strategy=load_strategy,
            resource_requirements=resource_requirements or {"cpu": "standard", "gpu": False, "memory_mb": 50},
            enabled=enabled,
            supported_platforms=supported_platforms or ["all"]
        )
        self._skills[name] = skill
        return skill

    def get(self, name: str) -> Optional[RegisteredSkill]:
        return self._skills.get(name)

    def get_all(self, enabled_only: bool = True) -> List[RegisteredSkill]:
        skills = list(self._skills.values())
        if enabled_only:
            skills = [s for s in skills if s.enabled]
        skills.sort(key=lambda s: s.priority)
        return skills

    def get_by_category(self, category: str) -> List[RegisteredSkill]:
        return [s for s in self.get_all() if s.category.lower() == category.lower()]

    def count(self) -> int:
        return len(self._skills)
