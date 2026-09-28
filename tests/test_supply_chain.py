"""Unit tests for the SupplyChainSecurityEngine, Attestation, and CompatibilityMatrix."""
from __future__ import annotations

import unittest
from pathlib import Path

from src.skills.compatibility import CompatibilityMatrix, SkillCompatibilityProfile
from src.skills.supply_chain import SecurityAttestation, SupplyChainSecurityEngine

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestSupplyChain(unittest.TestCase):
    """Test suite for supply chain, attestation, SBOM, and compatibility."""

    def setUp(self):
        self.sc = SupplyChainSecurityEngine(workspace_root=REPO_ROOT)
        self.cm = CompatibilityMatrix(workspace_root=REPO_ROOT)

    def test_scan_skill(self):
        att = self.sc.scan_skill("databases.postgresql")
        self.assertIsInstance(att, SecurityAttestation)
        self.assertEqual(att.skill_id, "databases.postgresql")
        self.assertIn(att.security_grade, ["A", "B", "C", "D", "F"])
        self.assertTrue(att.passed)
        self.assertGreater(len(att.sha256), 20)

    def test_generate_repository_sbom(self):
        sbom = self.sc.generate_repository_sbom()
        self.assertEqual(sbom.get("bomFormat"), "CycloneDX")
        self.assertEqual(sbom.get("specVersion"), "1.5")
        self.assertGreater(len(sbom.get("components", [])), 50)

    def test_compatibility_matrix(self):
        prof = self.cm.get_skill_profile("databases.postgresql")
        self.assertIsInstance(prof, SkillCompatibilityProfile)
        self.assertEqual(prof.skill_id, "databases.postgresql")
        self.assertIn("claude", prof.models)
        self.assertIn("gpt", prof.models)

        table = self.cm.format_matrix_table(["databases.postgresql"])
        self.assertIn("databases.postgresql", table)
        self.assertIn("Claude", table)


if __name__ == "__main__":
    unittest.main()
