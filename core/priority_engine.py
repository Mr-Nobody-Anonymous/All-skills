"""
Core Priority Engine.
Evaluates priority tiers and enforces execution latency budgets.
"""

from typing import Dict, List, Optional, Any
import logging

from scratch_priority_import.priority_levels import PriorityTier, get_tier_for_skill, get_tier_priority
from scratch_priority_import.priority_queue import SkillPriorityQueue

logger = logging.getLogger(__name__)


class PriorityEngine:
    """Schedules and executes skill events respecting tier boundaries."""

    def __init__(self):
        self.queue = SkillPriorityQueue()

    def schedule_task(self, task_name: str, payload: Any, tier: PriorityTier = PriorityTier.TIER_4_STANDARD) -> None:
        """Enqueue task according to priority tier."""
        self.queue.put({"name": task_name, "payload": payload}, tier=tier)

    def get_next_task(self) -> Optional[Dict[str, Any]]:
        """Retrieve highest priority task."""
        return self.queue.get()

    def get_skill_tier(self, skill_name: str, category: Optional[str] = None) -> PriorityTier:
        """Determine tier for a skill."""
        return get_tier_for_skill(skill_name, category)
