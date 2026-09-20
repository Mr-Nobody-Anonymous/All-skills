"""Unit tests for platform upgrades: Dependency Graph, Lockfile, Policy Engine, and Stats."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"

import sys
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.graph import SkillGraph
from skills.lock import SkillLockManager
from skills.policy import PolicyEngine, PolicyVerdict, RiskLevel


class TestPlatformUpgrades(unittest.TestCase):
    def setUp(self):
        self.workspace_root = _ROOT

    def test_graph_react_dependencies(self):
        graph = SkillGraph(self.workspace_root)
        deps = graph.get_dependencies("react")
        self.assertIn("typescript", deps)
        self.assertIn("accessibility", deps)
        self.assertIn("state-management", deps)

    def test_graph_nextjs_dependencies(self):
        graph = SkillGraph(self.workspace_root)
        deps = graph.get_dependencies("nextjs")
        self.assertIn("react", deps)
        self.assertIn("typescript", deps)
        self.assertIn("database", deps)

    def test_graph_dependents(self):
        graph = SkillGraph(self.workspace_root)
        dependents = graph.get_dependents("typescript")
        self.assertIn("react", dependents)
        self.assertIn("nextjs", dependents)

    def test_graph_conflicts(self):
        graph = SkillGraph(self.workspace_root)
        conflicts = graph.get_conflicts("react")
        conflict_targets = [c["conflicts_with"] for c in conflicts]
        self.assertIn("angular-state-management", conflict_targets)

    def test_lockfile_generation_and_verification(self):
        mgr = SkillLockManager(self.workspace_root)
        lock_data = mgr.generate_lockfile()
        self.assertEqual(lock_data["version"], 1)
        self.assertIn("react-state-management", lock_data["skills"])

        # Test verification of locked skill
        res = mgr.verify_skill("react-state-management")
        self.assertEqual(res["status"], "verified")
        self.assertTrue(res["hash_valid"])

    def test_policy_allow_safe_skill(self):
        pe = PolicyEngine(self.workspace_root)
        result = pe.evaluate_skill("react-state-management", ["file_read", "file_edit"])
        self.assertEqual(result.overall_verdict, PolicyVerdict.ALLOW)

    def test_policy_ask_critical_skill(self):
        pe = PolicyEngine(self.workspace_root)
        result = pe.evaluate_skill("direct-production-deployment", ["deploy"])
        self.assertEqual(result.overall_verdict, PolicyVerdict.ASK)
        self.assertEqual(result.max_risk, RiskLevel.CRITICAL)

    def test_policy_deny_secrets_skill(self):
        pe = PolicyEngine(self.workspace_root)
        result = pe.evaluate_skill("secrets-management", ["credentials"])
        self.assertEqual(result.overall_verdict, PolicyVerdict.DENY)


if __name__ == "__main__":
    unittest.main()
