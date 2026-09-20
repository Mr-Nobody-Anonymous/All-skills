"""Unit tests for SkillManager."""

import unittest
from core.skill_manager import SkillManager
from scratch_priority_import.skill_registry import SkillMetadata
from scratch_priority_import.priority_levels import PriorityTier


class TestSkillManager(unittest.TestCase):
    def setUp(self):
        self.sm = SkillManager()
        self.sm.registry.reset()

    def test_manager_initialization(self):
        meta = SkillMetadata(
            name="skill-time",
            category="productivity",
            priority_tier=PriorityTier.TIER_1_ESSENTIAL,
            dependencies=[]
        )
        self.sm.registry.register_metadata(meta)

        res = self.sm.initialize()
        self.assertGreaterEqual(res["loaded_count"], 1)
        self.assertTrue(self.sm.disable_skill("skill-time"))


if __name__ == "__main__":
    unittest.main()
