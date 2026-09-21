"""
Skill Router - Routes classified intents to the correct skill handler.
"""
from __future__ import annotations
from typing import Any, Dict, List, Optional


class SkillRouter:
    """
    Routes a classified intent to the best matching registered skill.
    Uses priority registry for conflict resolution.
    """

    def __init__(self):
        self._skills: Dict[str, Any] = {}

    def register(self, skill_id: str, skill_instance) -> None:
        """Register a skill with its ID."""
        self._skills[skill_id] = skill_instance

    def route(self, intent: str, context: Dict[str, Any]) -> Optional[Any]:
        """Find the highest-priority skill that can handle this intent."""
        candidates = [
            (s.get_priority(), sid, s)
            for sid, s in self._skills.items()
            if s.can_handle(intent, context)
        ]
        if not candidates:
            return None
        candidates.sort(key=lambda x: x[0])
        return candidates[0][2]

    def route_all(self, intent: str, context: Dict[str, Any]) -> List[Any]:
        """Return all skills that can handle this intent, sorted by priority."""
        candidates = [
            (s.get_priority(), s)
            for s in self._skills.values()
            if s.can_handle(intent, context)
        ]
        candidates.sort(key=lambda x: x[0])
        return [s for _, s in candidates]

    def list_skills(self) -> List[str]:
        return list(self._skills.keys())
