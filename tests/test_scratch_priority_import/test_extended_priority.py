import unittest
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from scratch_priority_import.priority_registry import PriorityRegistry
from scratch_priority_import.dependency_resolver import DependencyResolver
from scratch_priority_import.import_order import ImportOrder

class TestExtendedPriorityImport(unittest.TestCase):
    def test_priority_registration(self):
        reg = PriorityRegistry()
        s1 = reg.register("tts_engine", priority=2, category="speech_audio")
        s2 = reg.register("music_player", priority=20, category="media", dependencies=["tts_engine"])
        self.assertEqual(reg.count(), 2)
        self.assertEqual(s1.priority, 2)
        self.assertEqual(s2.dependencies, ["tts_engine"])

    def test_dependency_resolver(self):
        res = DependencyResolver()
        res.add_skill("app", ["db", "auth"])
        res.add_skill("auth", ["db"])
        res.add_skill("db", [])
        order = res.resolve_order()
        self.assertLess(order.index("db"), order.index("auth"))
        self.assertLess(order.index("auth"), order.index("app"))

    def test_import_order_scheduling(self):
        reg = PriorityRegistry()
        reg.register("music_player", priority=20, dependencies=["tts"])
        reg.register("tts", priority=2)
        sched = ImportOrder(reg)
        order = [s.name for s in sched.compute_import_schedule()]
        self.assertLess(order.index("tts"), order.index("music_player"))

if __name__ == "__main__":
    unittest.main()
