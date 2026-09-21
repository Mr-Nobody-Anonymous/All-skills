"""
Abstract Base Class for All Skills.
Every skill in the system must inherit from BaseSkill.
"""
from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any, Dict


class BaseSkill(ABC):
    """
    BaseSkill defines the interface contract every skill must implement.
    Skills register themselves through the priority registry at load time.
    """

    @abstractmethod
    def can_handle(self, intent: str, context: Dict[str, Any]) -> bool:
        """Return True if this skill can handle the given intent + context."""

    @abstractmethod
    def handle(self, intent: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute the skill. Must return a dict with at minimum:
          {"status": "ok"|"error"|"degraded", "result": ..., "intent": intent}
        """

    @abstractmethod
    def get_priority(self) -> int:
        """
        Return the skill's static priority (1=highest, 100=lowest).
        Used by the priority registry for conflict resolution.
        """

    def load_model(self):
        """Lazy-load any heavy models. Called on first use."""

    def unload_model(self):
        """Release models from memory when not in use."""

    def health_check(self) -> Dict[str, Any]:
        """Return a health status dict for the skill."""
        return {"healthy": True}

    def __repr__(self):
        return f"<{self.__class__.__name__} priority={self.get_priority()}>"
