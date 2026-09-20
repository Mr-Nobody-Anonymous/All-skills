"""
Conflict Resolver for All-Skills.
Resolves collisions between skills competing for the same intent or utterance.
Supports confidence scoring, contextual disambiguation, priority tiers, and user overrides.
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
import logging

from .priority_levels import PriorityTier

logger = logging.getLogger(__name__)


@dataclass
class IntentCandidate:
    """A skill candidate offering to handle a given intent."""
    skill_name: str
    intent_name: str
    confidence: float              # 0.0 to 1.0 confidence score
    priority_tier: PriorityTier    # Tier 0 (Critical) to Tier 6 (Lazy)
    context_match: bool = False    # True if active dialog context matches
    user_pinned: bool = False      # True if user explicitly selected/pinned this skill
    latency_estimate_ms: float = 50.0

    @property
    def score(self) -> float:
        """
        Composite ranking score:
        - user_pinned: +100.0 (overrides all)
        - context_match: +10.0 (favors active conversation)
        - tier bonus: (6 - tier.value) * 2.0 (higher tier = higher bonus)
        - confidence base: confidence * 10.0
        """
        if self.user_pinned:
            return 1000.0 + self.confidence

        score = self.confidence * 10.0
        if self.context_match:
            score += 10.0
        
        tier_weight = (6 - int(self.priority_tier)) * 2.0
        score += tier_weight
        return score


class ConflictResolver:
    """Manages skill intent collisions and selects the optimal handler."""

    def __init__(self):
        self._user_preferences: Dict[str, str] = {}  # intent -> preferred_skill_name
        self._active_contexts: List[str] = []

    def set_user_preference(self, intent: str, preferred_skill: str) -> None:
        """Pin a specific skill to handle an intent."""
        self._user_preferences[intent] = preferred_skill
        logger.info(f"User preference set: {intent} -> {preferred_skill}")

    def clear_user_preference(self, intent: str) -> None:
        """Remove a pinned preference."""
        self._user_preferences.pop(intent, None)

    def set_active_contexts(self, contexts: List[str]) -> None:
        """Set currently active dialog contexts (e.g., ['media_playing', 'timer_active'])."""
        self._active_contexts = list(contexts)

    def resolve(self, candidates: List[IntentCandidate]) -> Optional[IntentCandidate]:
        """
        Evaluate all candidates for an utterance/intent collision and return winner.
        Returns None if candidate list is empty.
        """
        if not candidates:
            return None

        # Check for user override
        for cand in candidates:
            preferred = self._user_preferences.get(cand.intent_name)
            if preferred and preferred == cand.skill_name:
                cand.user_pinned = True

        # Sort descending by composite score, then by lowest latency
        ranked = sorted(
            candidates,
            key=lambda c: (c.score, -c.latency_estimate_ms),
            reverse=True
        )

        winner = ranked[0]
        if len(ranked) > 1:
            logger.info(
                f"Resolved intent '{winner.intent_name}' conflict: "
                f"Winner '{winner.skill_name}' (score {winner.score:.2f}) "
                f"over '{ranked[1].skill_name}' (score {ranked[1].score:.2f})"
            )
        return winner
