"""Unit tests for import manager and lazy loader."""

import unittest
from scratch_priority_import.skill_registry import EnhancedSkillRegistry, SkillMetadata
from scratch_priority_import.priority_levels import PriorityTier
from scratch_priority_import.import_manager import ImportManager
from scratch_priority_import.lazy_loader import LazyLoaderManager
from scratch_priority_import.circular_dependency_detector import CircularDependencyDetector, CircularDependencyError
from scratch_priority_import.dependency_graph import DependencyGraph


class TestImportManager(unittest.TestCase):
    def setUp(self):
        self.registry = EnhancedSkillRegistry()
        self.registry.reset()

        # Add mock skills across tiers
        self.registry.register_metadata(SkillMetadata(
            name="skill-time",
            category="productivity",
            priority_tier=PriorityTier.TIER_1_ESSENTIAL,
            dependencies=[]
        ))
        self.registry.register_metadata(SkillMetadata(
            name="skill-alarm",
            category="productivity",
            priority_tier=PriorityTier.TIER_1_ESSENTIAL,
            dependencies=["skill-time"]
        ))
        self.registry.register_metadata(SkillMetadata(
            name="skill-system",
            category="system",
            priority_tier=PriorityTier.TIER_0_CRITICAL,
            dependencies=[]
        ))
        self.registry.register_metadata(SkillMetadata(
            name="skill-garden",
            category="agriculture",
            priority_tier=PriorityTier.TIER_6_LAZY,
            dependencies=[]
        ))

        self.manager = ImportManager(self.registry, allow_lazy=True)

    def test_compute_import_order(self):
        order = self.manager.compute_import_order()
        # Ensure dependencies come before dependents
        self.assertIn("skill-time", order)
        self.assertIn("skill-alarm", order)
        self.assertTrue(order.index("skill-time") < order.index("skill-alarm"))

    def test_load_all_and_lazy_deferral(self):
        results = self.manager.load_all()
        # skill-garden is Tier 6 Lazy, so it is deferred via lazy proxy
        self.assertIn("skill-system", results["loaded_skills"])
        self.assertTrue(self.manager.lazy_manager.is_lazy("skill-garden"))

    def test_cycle_detection(self):
        graph = DependencyGraph()
        graph.add_dependency("a", "b")
        graph.add_dependency("b", "c")
        graph.add_dependency("c", "a")

        detector = CircularDependencyDetector(graph)
        self.assertTrue(detector.has_cycle())
        with self.assertRaises(CircularDependencyError):
            detector.validate()


class TestLazyLoader(unittest.TestCase):
    def test_lazy_proxy(self):
        lazy = LazyLoaderManager()
        invoked = False

        def mock_loader():
            nonlocal invoked
            invoked = True
            return {"name": "heavy-model", "ready": True}

        proxy = lazy.register_lazy("heavy-model", mock_loader)
        self.assertFalse(invoked)
        self.assertFalse(proxy.is_loaded)

        # Access attribute triggers instantiation
        val = proxy["ready"]
        self.assertTrue(invoked)
        self.assertTrue(proxy.is_loaded)
        self.assertTrue(val)


if __name__ == "__main__":
    unittest.main()
