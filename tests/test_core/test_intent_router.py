"""Unit tests for IntentRouter."""

import unittest
from core.intent_router import IntentRouter
from scratch_priority_import.priority_levels import PriorityTier


class TestIntentRouter(unittest.TestCase):
    def setUp(self):
        self.router = IntentRouter()

    def test_routing_and_execution(self):
        called = False

        def handler(params):
            nonlocal called
            called = True
            return "Volume changed"

        self.router.register_intent(
            skill_name="skill-volume",
            intent_name="volume_up",
            patterns=[r"volume up", r"turn it up"],
            handler=handler,
            tier=PriorityTier.TIER_0_CRITICAL
        )

        res = self.router.route("please turn it up now")
        self.assertTrue(called)
        self.assertEqual(res, "Volume changed")


if __name__ == "__main__":
    unittest.main()
