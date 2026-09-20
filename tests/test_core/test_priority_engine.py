"""Unit tests for PriorityEngine."""

import unittest
from core.priority_engine import PriorityEngine
from scratch_priority_import.priority_levels import PriorityTier


class TestPriorityEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PriorityEngine()

    def test_priority_scheduling(self):
        self.engine.schedule_task("low_task", {"val": 1}, tier=PriorityTier.TIER_5_LOW)
        self.engine.schedule_task("crit_task", {"val": 2}, tier=PriorityTier.TIER_0_CRITICAL)

        task = self.engine.get_next_task()
        self.assertIsNotNone(task)
        self.assertEqual(task["name"], "crit_task")


if __name__ == "__main__":
    unittest.main()
