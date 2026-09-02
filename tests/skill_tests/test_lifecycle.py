"""Tests for the skill lifecycle state machine (P1)."""
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.lifecycle import LIFECYCLE_STATES, can_transition, is_active, is_valid, transition  # noqa: E402


class TestLifecycle(unittest.TestCase):
    def test_all_states_valid(self):
        for state in LIFECYCLE_STATES:
            self.assertTrue(is_valid(state), state)
        self.assertFalse(is_valid("mystery"))

    def test_enabled_is_active_only(self):
        self.assertTrue(is_active("enabled"))
        self.assertFalse(is_active("disabled"))
        self.assertFalse(is_active("quarantined"))
        self.assertFalse(is_active("ready"))

    def test_forward_transitions(self):
        self.assertTrue(can_transition("discovered", "imported"))
        self.assertTrue(can_transition("validated", "security_scanned"))
        self.assertTrue(can_transition("ready", "enabled"))
        self.assertFalse(can_transition("enabled", "security_scanned"))
        self.assertFalse(can_transition("deprecated", "ready"))

    def test_transition_returns_target(self):
        self.assertEqual(transition("ready", "enabled"), "enabled")

    def test_invalid_transition_raises(self):
        with self.assertRaises(ValueError):
            transition("enabled", "security_scanned")

    def test_unknown_state_raises(self):
        with self.assertRaises(ValueError):
            transition("ready", "wat")


if __name__ == "__main__":
    unittest.main()