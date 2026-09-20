"""Unit tests for enhanced skill registry and versioning."""

import unittest
from scratch_priority_import.skill_registry import EnhancedSkillRegistry, SkillMetadata
from scratch_priority_import.priority_levels import PriorityTier
from scratch_priority_import.version_checker import VersionChecker, SemanticVersion
from scratch_priority_import.compatibility_checker import CompatibilityChecker


class TestEnhancedSkillRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = EnhancedSkillRegistry()
        self.registry.reset()

    def test_register_and_query_metadata(self):
        meta = SkillMetadata(
            name="skill-ovos-weather",
            category="weather",
            priority_tier=PriorityTier.TIER_1_ESSENTIAL,
            version="1.2.0",
            dependencies=["skill-date-time"],
            intents=["get_weather", "get_forecast"],
            description="Weather forecasting skill"
        )
        self.registry.register_metadata(meta)

        retrieved = self.registry.get_metadata("skill-ovos-weather")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.version, "1.2.0")
        self.assertEqual(retrieved.priority_tier, PriorityTier.TIER_1_ESSENTIAL)

        # Query by tier
        tier1_skills = self.registry.get_by_tier(PriorityTier.TIER_1_ESSENTIAL)
        self.assertTrue(any(s.name == "skill-ovos-weather" for s in tier1_skills))


class TestVersionAndCompatibility(unittest.TestCase):
    def test_semantic_version_comparisons(self):
        v1 = SemanticVersion("1.0.0")
        v2 = SemanticVersion("1.2.0")
        v3 = SemanticVersion("2.0.0")

        self.assertTrue(v1 < v2)
        self.assertTrue(v2 < v3)
        self.assertEqual(v1, "1.0.0")

    def test_version_satisfaction(self):
        self.assertTrue(VersionChecker.satisfies("1.2.3", ">=1.0.0"))
        self.assertTrue(VersionChecker.satisfies("1.2.3", ">=1.0.0, <2.0.0"))
        self.assertTrue(VersionChecker.satisfies("1.5.0", "^1.2.0"))
        self.assertFalse(VersionChecker.satisfies("2.0.0", "^1.2.0"))
        self.assertFalse(VersionChecker.satisfies("0.9.0", ">=1.0.0"))

    def test_compatibility_checker(self):
        checker = CompatibilityChecker()
        res = checker.evaluate_skill("test-skill", supported_platforms=["windows", "linux", "darwin"], min_python="3.7")
        self.assertTrue(res["compatible"])
        self.assertTrue(res["python_ok"])


if __name__ == "__main__":
    unittest.main()
