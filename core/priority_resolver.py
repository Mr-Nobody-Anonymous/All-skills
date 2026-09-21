"""
Priority Resolver for All-Skills Platform.
Resolves execution order and intent collisions based on priority ranks (1-100),
context history, user preferences, and dependency topology.
"""

from typing import List, Dict, Any, Optional

class PriorityResolver:
    def __init__(self):
        self.user_overrides: Dict[str, str] = {}

    def set_user_override(self, intent: str, preferred_skill_id: str):
        self.user_overrides[intent] = preferred_skill_id

    def resolve(self, candidates: List[Dict[str, Any]], context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Resolves the best candidate skill.
        Candidate dict expected fields:
          - skill_id: str
          - priority: int (1-100, lower number = higher priority)
          - confidence: float (0.0 to 1.0)
          - intent: str
        """
        if not candidates:
            return None

        intent = candidates[0].get("intent")
        if intent and intent in self.user_overrides:
            override_id = self.user_overrides[intent]
            for c in candidates:
                if c.get("skill_id") == override_id:
                    return c

        def score(c):
            # Combined rank score: high confidence bonus, lower priority rank penalty
            priority = c.get("priority", 50)
            confidence = c.get("confidence", 0.5)
            context_bonus = 0.2 if context and context.get("last_skill") == c.get("skill_id") else 0.0
            return (confidence + context_bonus) * 100 - priority

        sorted_candidates = sorted(candidates, key=score, reverse=True)
        return sorted_candidates[0]
