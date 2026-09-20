"""Unit tests for core ConflictResolver."""

import unittest
from core.conflict_resolver import ConflictResolver, IntentCandidate
from scratch_priority_import.priority_levels import PriorityTier


class TestCoreConflictResolver(unittest.TestCase):
    def test_conflict_resolution(self):
        resolver = ConflictResolver()
        c1 = IntentCandidate("skill-a", "intent", 0.5, PriorityTier.TIER_1_ESSENTIAL)
        c2 = IntentCandidate("skill-b", "intent", 0.5, PriorityTier.TIER_5_LOW)
        winner = resolver.resolve([c1, c2])
        self.assertEqual(winner.skill_name, "skill-a")


if __name__ == "__main__":
    unittest.main()
