"""
Core Intent Router.
Routes natural language utterances to registered skills using regex, keyword, and parser plugins.
Falls back gracefully through FallbackChain when confidence is low.
"""

import re
from typing import Dict, List, Callable, Optional, Any
import logging

from scratch_priority_import.conflict_resolver import ConflictResolver, IntentCandidate
from scratch_priority_import.priority_levels import PriorityTier
from scratch_priority_import.fallback_chain import FallbackChain

logger = logging.getLogger(__name__)


class RegisteredIntent:
    """Descriptor for a registered skill intent."""
    def __init__(self, skill_name: str, intent_name: str, patterns: List[str], handler: Callable[[Dict[str, str]], Any], tier: PriorityTier = PriorityTier.TIER_4_STANDARD):
        self.skill_name = skill_name
        self.intent_name = intent_name
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.handler = handler
        self.tier = tier


class IntentRouter:
    """Parses utterances and dispatches messages to skills."""

    def __init__(self):
        self._intents: List[RegisteredIntent] = []
        self.conflict_resolver = ConflictResolver()
        self.fallback_chain = FallbackChain()

    def register_intent(
        self,
        skill_name: str,
        intent_name: str,
        patterns: List[str],
        handler: Callable[[Dict[str, str]], Any],
        tier: PriorityTier = PriorityTier.TIER_4_STANDARD
    ) -> None:
        """Register an intent pattern."""
        self._intents.append(RegisteredIntent(skill_name, intent_name, patterns, handler, tier))

    def route(self, utterance: str) -> Optional[Any]:
        """Match utterance against registered intents or invoke fallback chain."""
        candidates: List[IntentCandidate] = []
        matches: Dict[str, Dict[str, Any]] = {}

        for intent in self._intents:
            for pattern in intent.patterns:
                match = pattern.search(utterance)
                if match:
                    # Calculate simple confidence
                    matched_len = len(match.group(0))
                    confidence = min(1.0, matched_len / max(1, len(utterance.strip())))
                    cand = IntentCandidate(
                        skill_name=intent.skill_name,
                        intent_name=intent.intent_name,
                        confidence=confidence,
                        priority_tier=intent.tier
                    )
                    candidates.append(cand)
                    matches[f"{intent.skill_name}:{intent.intent_name}"] = {
                        "handler": intent.handler,
                        "groups": match.groupdict()
                    }
                    break

        if candidates:
            winner = self.conflict_resolver.resolve(candidates)
            if winner:
                key = f"{winner.skill_name}:{winner.intent_name}"
                matched_data = matches.get(key)
                if matched_data:
                    return matched_data["handler"](matched_data["groups"])

        # Invoke fallback chain if no primary intent triggered
        logger.info(f"No primary intent for '{utterance}'. Invoking fallback chain...")
        fallback_res = self.fallback_chain.dispatch(utterance)
        return fallback_res
