"""Unit tests for the AI Skills Package Manager & Dependency System."""
from __future__ import annotations

import unittest
from pathlib import Path

from src.skills.package_manager import PackageManager, DependencyNode

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestPackageManager(unittest.TestCase):
    """Test suite for the PackageManager, why, tree resolution, and audit."""

    def setUp(self):
        self.pm = PackageManager(workspace_root=REPO_ROOT)

    def test_resolve_tree(self):
        node = self.pm.resolve_tree("databases.postgresql")
        self.assertIsInstance(node, DependencyNode)
        self.assertEqual(node.skill_id, "databases.postgresql")
        formatted = node.format_tree()
        self.assertIn("databases.postgresql", formatted)

    def test_why(self):
        res = self.pm.why("databases.postgresql")
        self.assertIn("skill_id", res)
        self.assertEqual(res["skill_id"], "databases.postgresql")
        self.assertGreaterEqual(len(res["why"]), 1)

    def test_audit(self):
        report = self.pm.audit()
        self.assertIn("status", report)
        self.assertIn(report["status"], ["PASS", "FAIL"])
        self.assertIsInstance(report["findings"], list)

    def test_get_provenance(self):
        prov = self.pm.get_provenance("databases.postgresql")
        self.assertIn("source", prov)
        self.assertIn("license", prov)
        self.assertEqual(prov["license"], "MIT")


if __name__ == "__main__":
    unittest.main()
