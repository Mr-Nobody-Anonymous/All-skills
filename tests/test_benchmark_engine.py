"""Unit tests for the Skill Benchmark Evaluator, VersionComparator, and RealWorldBenchmarkRunner."""
from __future__ import annotations

import unittest
from pathlib import Path

from benchmarks.engine.evaluator import BenchmarkResult, SkillBenchmarkEvaluator
from benchmarks.engine.version_compare import VersionComparator, VersionComparisonReport
from benchmarks.real_world.runner import RealWorldBenchmarkRunner, ComparativeBenchmarkSummary

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestBenchmarkEngine(unittest.TestCase):
    """Test suite for benchmarking engine and version comparison."""

    def setUp(self):
        self.evaluator = SkillBenchmarkEvaluator(workspace_root=REPO_ROOT)
        self.runner = RealWorldBenchmarkRunner(workspace_root=REPO_ROOT)

    def test_evaluate_skill(self):
        res = self.evaluator.evaluate_skill("databases.postgresql")
        self.assertIsInstance(res, BenchmarkResult)
        self.assertEqual(res.skill_id, "databases.postgresql")
        self.assertGreaterEqual(res.composite_score, 50.0)
        self.assertGreaterEqual(res.avg_token_cost, 500)
        self.assertGreaterEqual(res.task_completion_pct, 50.0)

        card = res.summary_card()
        self.assertIn("Composite Score:", card)
        self.assertIn("databases.postgresql", card)

    def test_version_comparator(self):
        r1 = self.evaluator.evaluate_skill("databases.postgresql", version="1.2.0")
        r2 = self.evaluator.evaluate_skill("databases.postgresql", version="1.3.0")
        r2.correctness_pct = min(100.0, r1.correctness_pct + 5.0)
        r2.composite_score = min(100.0, r1.composite_score + 4.0)

        report = VersionComparator.analyze_history("databases.postgresql", [r1, r2])
        self.assertIsInstance(report, VersionComparisonReport)
        self.assertEqual(len(report.diffs), 1)
        self.assertFalse(report.diffs[0].is_regression)

        # Test regression detection
        r3 = self.evaluator.evaluate_skill("databases.postgresql", version="1.4.0")
        r3.composite_score = r2.composite_score - 5.0
        r3.correctness_pct = r2.correctness_pct - 6.0
        reg_diff = VersionComparator.compare_two(r2, r3)
        self.assertTrue(reg_diff.is_regression)
        self.assertGreater(len(reg_diff.regression_reasons), 0)

    def test_real_world_runner(self):
        summary = self.runner.run_benchmark()
        self.assertIsInstance(summary, ComparativeBenchmarkSummary)
        self.assertGreaterEqual(summary.with_allskills_success_pct, summary.without_allskills_success_pct)
        self.assertLess(summary.token_reduction_pct, 0.0)  # negative means savings
        self.assertLess(summary.failure_reduction_pct, 0.0)


if __name__ == "__main__":
    unittest.main()
