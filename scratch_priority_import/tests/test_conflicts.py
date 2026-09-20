"""Unit tests for conflict resolution and fallback chains."""

import unittest
from scratch_priority_import.conflict_resolver import ConflictResolver, IntentCandidate
from scratch_priority_import.priority_levels import PriorityTier
from scratch_priority_import.fallback_chain import FallbackChain


class TestConflictResolver(unittest.TestCase):
    def setUp(self):
        self.resolver = ConflictResolver()

    def test_confidence_and_tier_resolution(self):
        # Candidate 1: High tier, confidence 0.8
        c1 = IntentCandidate(
            skill_name="skill-ovos-media",
            intent_name="play_music",
            confidence=0.8,
            priority_tier=PriorityTier.TIER_2_HIGH
        )
        # Candidate 2: Low tier, confidence 0.8
        c2 = IntentCandidate(
            skill_name="skill-youtube",
            intent_name="play_music",
            confidence=0.8,
            priority_tier=PriorityTier.TIER_5_LOW
        )

        winner = self.resolver.resolve([c1, c2])
        self.assertIsNotNone(winner)
        self.assertEqual(winner.skill_name, "skill-ovos-media")

    def test_context_match_bonus(self):
        # Candidate 1: confidence 0.9, no context match
        c1 = IntentCandidate(
            skill_name="skill-radio",
            intent_name="stop_playback",
            confidence=0.9,
            priority_tier=PriorityTier.TIER_2_HIGH,
            context_match=False
        )
        # Candidate 2: confidence 0.7, active context match
        c2 = IntentCandidate(
            skill_name="skill-spotify",
            intent_name="stop_playback",
            confidence=0.7,
            priority_tier=PriorityTier.TIER_2_HIGH,
            context_match=True
        )

        winner = self.resolver.resolve([c1, c2])
        self.assertIsNotNone(winner)
        # c2 has context bonus (+10), so it wins over c1
        self.assertEqual(winner.skill_name, "skill-spotify")

    def test_user_preference_override(self):
        c1 = IntentCandidate(
            skill_name="skill-default-media",
            intent_name="play_audio",
            confidence=0.95,
            priority_tier=PriorityTier.TIER_1_ESSENTIAL
        )
        c2 = IntentCandidate(
            skill_name="skill-custom-media",
            intent_name="play_audio",
            confidence=0.5,
            priority_tier=PriorityTier.TIER_5_LOW
        )

        # Pin preference for c2
        self.resolver.set_user_preference("play_audio", "skill-custom-media")
        winner = self.resolver.resolve([c1, c2])
        self.assertEqual(winner.skill_name, "skill-custom-media")


class TestFallbackChain(unittest.TestCase):
    def test_fallback_chain_dispatch(self):
        chain = FallbackChain()
        chain.register_handler("wolfram", priority=10, handler_fn=lambda q: None)  # Fails
        chain.register_handler("chatgpt", priority=20, handler_fn=lambda q: f"GPT answer to {q}")

        res = chain.dispatch("What is quantum computing?")
        self.assertIsNotNone(res)
        self.assertEqual(res["handler"], "chatgpt")
        self.assertIn("GPT answer to What is quantum computing?", res["response"])


if __name__ == "__main__":
    unittest.main()
