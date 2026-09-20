"""Unit tests for priority levels and priority queue."""

import unittest
from scratch_priority_import.priority_levels import (
    PriorityTier,
    get_tier_for_skill,
    get_tier_priority,
    DEFAULT_TIER_MAPPING,
)
from scratch_priority_import.priority_queue import SkillPriorityQueue


class TestPriorityLevels(unittest.TestCase):
    def test_tier_enumeration(self):
        self.assertEqual(int(PriorityTier.TIER_0_CRITICAL), 0)
        self.assertEqual(int(PriorityTier.TIER_1_ESSENTIAL), 1)
        self.assertEqual(int(PriorityTier.TIER_2_HIGH), 2)
        self.assertEqual(int(PriorityTier.TIER_3_MEDIUM), 3)
        self.assertEqual(int(PriorityTier.TIER_4_STANDARD), 4)
        self.assertEqual(int(PriorityTier.TIER_5_LOW), 5)
        self.assertEqual(int(PriorityTier.TIER_6_LAZY), 6)

    def test_from_name_and_aliases(self):
        self.assertEqual(PriorityTier.from_name("CRITICAL"), PriorityTier.TIER_0_CRITICAL)
        self.assertEqual(PriorityTier.from_name("TIER_0_CRITICAL"), PriorityTier.TIER_0_CRITICAL)
        self.assertEqual(PriorityTier.from_name("ESSENTIAL"), PriorityTier.TIER_1_ESSENTIAL)
        self.assertEqual(PriorityTier.from_name("HIGH"), PriorityTier.TIER_2_HIGH)
        self.assertEqual(PriorityTier.from_name("MEDIUM"), PriorityTier.TIER_3_MEDIUM)
        self.assertEqual(PriorityTier.from_name("STANDARD"), PriorityTier.TIER_4_STANDARD)
        self.assertEqual(PriorityTier.from_name("LOW"), PriorityTier.TIER_5_LOW)
        self.assertEqual(PriorityTier.from_name("LAZY"), PriorityTier.TIER_6_LAZY)

    def test_skill_tier_inference(self):
        self.assertEqual(get_tier_for_skill("skill-volume"), PriorityTier.TIER_0_CRITICAL)
        self.assertEqual(get_tier_for_skill("skill-weather"), PriorityTier.TIER_1_ESSENTIAL)
        self.assertEqual(get_tier_for_skill("skill-calendar"), PriorityTier.TIER_2_HIGH)
        self.assertEqual(get_tier_for_skill("skill-home-assistant"), PriorityTier.TIER_3_MEDIUM)
        self.assertEqual(get_tier_for_skill("skill-wikipedia"), PriorityTier.TIER_4_STANDARD)
        self.assertEqual(get_tier_for_skill("skill-jokes"), PriorityTier.TIER_5_LOW)
        self.assertEqual(get_tier_for_skill("skill-obd"), PriorityTier.TIER_6_LAZY)


class TestPriorityQueue(unittest.TestCase):
    def test_queue_ordering(self):
        q = SkillPriorityQueue()
        q.put("low_task", priority=50, tier=PriorityTier.TIER_5_LOW)
        q.put("crit_task", priority=0, tier=PriorityTier.TIER_0_CRITICAL)
        q.put("high_task", priority=20, tier=PriorityTier.TIER_2_HIGH)

        self.assertEqual(q.qsize(), 3)
        self.assertEqual(q.get(), "crit_task")
        self.assertEqual(q.get(), "high_task")
        self.assertEqual(q.get(), "low_task")
        self.assertTrue(q.is_empty())


if __name__ == "__main__":
    unittest.main()
