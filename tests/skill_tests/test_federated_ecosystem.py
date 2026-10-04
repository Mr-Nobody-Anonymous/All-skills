"""Unit and regression tests for the Federated Skill Ecosystem."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

from ingestion.pipeline import IngestionPipeline
from vendor.nvidia_skillevaluator.evaluator import SkillEvaluator
from benchmarks.retrieval.retrieval_benchmark import RetrievalBenchmark
from src.skills.registry import Registry, TrustTier
from src.skills.router import Router
from src.skills.frontmatter import parse_frontmatter


class TestFederatedEcosystem(unittest.TestCase):
    """Test suite verifying the federated architecture, ingestion, provenance, and evaluation."""

    def test_sources_architecture(self):
        sources_dir = REPO_ROOT / "sources"
        self.assertTrue((sources_dir / "official").is_dir())
        self.assertTrue((sources_dir / "community").is_dir())
        self.assertTrue((sources_dir / "catalogs").is_dir())

        # Check official sources
        for official in ["anthropics", "openai", "github", "microsoft", "google"]:
            p = sources_dir / "official" / official
            self.assertTrue(p.is_dir(), f"Missing official source {official}")
            self.assertTrue((p / "source_info.json").is_file())
            self.assertTrue((p / "LICENSE").is_file())

    def test_staging_architecture(self):
        staging_dir = REPO_ROOT / "staging"
        for folder in ["anthropics", "openai", "github", "microsoft", "kdense", "ecc", "community"]:
            self.assertTrue((staging_dir / folder).is_dir())

    def test_ingestion_pipeline_stages(self):
        pipeline = IngestionPipeline(REPO_ROOT)
        for stage in IngestionPipeline.STAGES:
            stage_dir = REPO_ROOT / "ingestion" / stage
            self.assertTrue(stage_dir.is_dir(), f"Missing stage directory {stage}")

        # Test discovery recording
        rec = pipeline.discover("test-src", "https://github.com/example/repo", "main", "MIT")
        self.assertEqual(rec["source_id"], "test-src")
        discovery_file = REPO_ROOT / "ingestion" / "00_discovered" / "test-src.json"
        self.assertTrue(discovery_file.is_file())
        discovery_file.unlink()

    def test_registry_metadata_integrity(self):
        reg_dir = REPO_ROOT / "registry"

        # 1. sources.json
        sources_json = json.loads((reg_dir / "sources.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(sources_json.get("sources", [])), 14)

        # 2. licenses.json
        licenses_json = json.loads((reg_dir / "licenses.json").read_text(encoding="utf-8"))
        self.assertIn("spdx_approved_licenses", licenses_json)
        self.assertIn("source_licenses", licenses_json)
        self.assertIn("per_skill_licenses", licenses_json)

        # 3. trust.json
        trust_json = json.loads((reg_dir / "trust.json").read_text(encoding="utf-8"))
        self.assertIn("ladder", trust_json)
        self.assertIn("T5_CURATED", trust_json["ladder"])

        # 4. provenance.json
        prov_json = json.loads((reg_dir / "provenance.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(prov_json.get("total_canonical_skills", 0), 200)

        # 5. revocations.json
        rev_json = json.loads((reg_dir / "revocations.json").read_text(encoding="utf-8"))
        self.assertIn("revoked_sources", rev_json)

    def test_canonical_skills_expansion_domains(self):
        skills_dir = REPO_ROOT / "skills"
        expected_domains = [
            "mobile", "data", "databases", "scientific", "legal", "embedded",
            "game", "desktop", "os", "networking", "cloud", "finops",
            "ai", "security", "observability", "product", "education",
            "finance", "creative"
        ]
        for dom in expected_domains:
            dom_path = skills_dir / dom
            self.assertTrue(dom_path.is_dir(), f"Canonical domain directory missing: {dom}")
            skill_mds = list(dom_path.glob("*/SKILL.md"))
            self.assertGreater(len(skill_mds), 0, f"Domain {dom} has no canonical skills")

    def test_nvidia_skillevaluator(self):
        evaluator = SkillEvaluator(REPO_ROOT)
        test_skill = REPO_ROOT / "skills" / "mobile" / "android-compose" / "SKILL.md"
        self.assertTrue(test_skill.is_file())

        report = evaluator.evaluate_full(test_skill)
        self.assertTrue(report.tier1.valid_schema)
        self.assertTrue(report.tier1.security_clean)
        self.assertGreaterEqual(report.tier1.quality_score, 7.0)
        self.assertEqual(report.overall_verdict, "PASSED")

    def test_sra_retrieval_benchmark(self):
        benchmark = RetrievalBenchmark(REPO_ROOT)
        res = benchmark.run_benchmark()
        self.assertGreaterEqual(res.precision_at_3, 0.90, "Retrieval Precision@3 should be >= 90%")
        self.assertGreaterEqual(res.mrr, 0.85, "Mean Reciprocal Rank should be >= 0.85")


if __name__ == "__main__":
    unittest.main()
