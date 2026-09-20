import unittest
import tempfile
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scratch_priority_import.registry import (
    SkillRegistry,
    SkillModule,
    SkillDomain,
    SkillLevel,
)
from scratch_priority_import.priority import PriorityManager
from scratch_priority_import.resolver import DependencyResolver, CircularDependencyError
from scratch_priority_import.loader import SkillLoader
from scratch_priority_import.catalog import get_full_catalog
from scratch_priority_import.config import SkillConfig
from scratch_priority_import.utils import format_slug, render_ascii_tree


class TestSkillRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = SkillRegistry()
        self.registry.reset()

    def test_register_and_get(self):
        s = SkillModule(
            name="test.skill",
            domain=SkillDomain.PROGRAMMING,
            level=SkillLevel.CORE,
            priority=10,
            description="Test skill description"
        )
        self.registry.register(s)
        self.assertEqual(self.registry.count, 1)
        retrieved = self.registry.get("test.skill")
        self.assertIsNotNone(retrieved)
        self.assertEqual(retrieved.name, "test.skill")

    def test_search(self):
        s = SkillModule(
            name="docker.container",
            domain=SkillDomain.DEVOPS,
            level=SkillLevel.CORE,
            priority=5,
            tags=["container", "docker", "ops"],
            description="Manage docker containers"
        )
        self.registry.register(s)
        results = self.registry.search("docker")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "docker.container")

    def test_domain_filtering(self):
        s1 = SkillModule(name="p1", domain=SkillDomain.PROGRAMMING, level=SkillLevel.CORE, priority=1)
        s2 = SkillModule(name="p2", domain=SkillDomain.AI_ML, level=SkillLevel.CORE, priority=1)
        self.registry.register_batch([s1, s2])
        self.assertEqual(len(self.registry.get_by_domain(SkillDomain.PROGRAMMING)), 1)
        self.assertEqual(len(self.registry.get_by_domain(SkillDomain.AI_ML)), 1)


class TestPriorityAndResolution(unittest.TestCase):
    def setUp(self):
        self.registry = SkillRegistry()
        self.registry.reset()
        
        # Build dependency chain: A -> B -> C
        self.s_a = SkillModule(name="skill.a", domain=SkillDomain.PROGRAMMING, level=SkillLevel.FUNDAMENTAL, priority=0)
        self.s_b = SkillModule(name="skill.b", domain=SkillDomain.PROGRAMMING, level=SkillLevel.CORE, priority=10, dependencies=["skill.a"])
        self.s_c = SkillModule(name="skill.c", domain=SkillDomain.PROGRAMMING, level=SkillLevel.ADVANCED, priority=20, dependencies=["skill.b"])
        self.registry.register_batch([self.s_a, self.s_b, self.s_c])
        
        self.resolver = DependencyResolver(self.registry)
        self.pm = PriorityManager(self.registry)

    def test_topological_resolution(self):
        order = self.resolver.resolve("skill.c")
        self.assertEqual(order, ["skill.a", "skill.b", "skill.c"])

    def test_circular_dependency_detection(self):
        # Create cycle
        self.registry.register(SkillModule(name="cycle.1", domain=SkillDomain.PROGRAMMING, level=SkillLevel.CORE, priority=1, dependencies=["cycle.2"]))
        self.registry.register(SkillModule(name="cycle.2", domain=SkillDomain.PROGRAMMING, level=SkillLevel.CORE, priority=1, dependencies=["cycle.1"]))
        
        with self.assertRaises(CircularDependencyError):
            self.resolver.resolve("cycle.1")

    def test_dependency_tree(self):
        tree = self.resolver.get_dependency_tree("skill.c")
        self.assertEqual(tree["name"], "skill.c")
        self.assertIn("skill.b", tree["dependencies"])
        ascii_out = render_ascii_tree(tree)
        self.assertIn("skill.c", ascii_out)
        self.assertIn("skill.b", ascii_out)


class TestDefaultCatalogIntegrity(unittest.TestCase):
    def setUp(self):
        self.registry = SkillRegistry()
        self.registry.reset()
        self.loader = SkillLoader(registry=self.registry)
        self.loader.register_all_default_skills()

    def test_catalog_size(self):
        self.assertGreater(self.registry.count, 50)

    def test_zero_cycles_in_default_catalog(self):
        cycles = self.loader.resolver.find_cycles()
        self.assertEqual(len(cycles), 0, f"Found cycles in default catalog: {cycles}")

    def test_zero_missing_dependencies(self):
        missing = self.loader.priority_manager.validate_dependencies()
        self.assertEqual(len(missing), 0, f"Found missing dependencies in default catalog: {missing}")


class TestSkillConfig(unittest.TestCase):
    def test_save_and_load_yaml(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = Path(tmpdir) / "test_config.yaml"
            cfg = SkillConfig(max_workers=6, log_level="DEBUG", enabled_domains=["programming", "ai_ml"])
            cfg.to_file(str(cfg_path))
            
            loaded = SkillConfig.from_file(str(cfg_path))
            self.assertEqual(loaded.max_workers, 6)
            self.assertEqual(loaded.log_level, "DEBUG")
            self.assertIn("programming", loaded.enabled_domains)


if __name__ == "__main__":
    unittest.main()
