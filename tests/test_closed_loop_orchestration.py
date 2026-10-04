"""Unit tests for the Closed-Loop Orchestration Engine:

IntentAnalyzer, SkillComposer, ExplainabilityTracer, ConflictResolver, and LearningEngine.
"""
from __future__ import annotations

import unittest
import tempfile
from pathlib import Path

from src.skills.composer import SkillComposer, SkillStack
from src.skills.conflicts import ConflictResolver, load_conflicts
from src.skills.explain import ExplainabilityReport, ExplainabilityTracer
from src.skills.intent import AnalyzedIntent, IntentAnalyzer
from src.skills.learning import LearningEngine, TaskExecutionRecord
from src.skills.registry import load_registry

REPO_ROOT = Path(__file__).resolve().parents[1]


class TestClosedLoopOrchestration(unittest.TestCase):
    """Test suite for the closed-loop agent capability orchestration engine."""

    def setUp(self):
        self.registry = load_registry(REPO_ROOT)
        self.composer = SkillComposer(registry=self.registry, workspace_root=REPO_ROOT)
        self.intent_analyzer = IntentAnalyzer()
        self.conflict_resolver = ConflictResolver()
        self.telemetry_workspace = tempfile.TemporaryDirectory(prefix="all-skills-telemetry-")
        self.addCleanup(self.telemetry_workspace.cleanup)
        self.learning_engine = LearningEngine(workspace_root=Path(self.telemetry_workspace.name))

    def test_intent_analyzer_basic(self):
        query = "Build an e-commerce checkout with Stripe and PostgreSQL without mongodb"
        intent = self.intent_analyzer.analyze(query)

        self.assertEqual(intent.action_type, "build")
        self.assertIn("payments", intent.slots_needed)
        self.assertIn("database", intent.slots_needed)
        self.assertIn("stripe", intent.explicit_mentions)
        self.assertIn("postgresql", intent.explicit_mentions)
        self.assertIn("mongodb", intent.negative_preferences)

    def test_skill_composer_stack(self):
        query = "Build a SaaS dashboard with Stripe payments and PostgreSQL"
        stack = self.composer.compose(query)

        self.assertIsInstance(stack, SkillStack)
        self.assertGreaterEqual(len(stack.skills), 2)
        self.assertTrue(any("db" in s or "database" in s or "postgre" in s for s in stack.skills))
        self.assertGreaterEqual(stack.quality_score, 50.0)

        # Verify explainability report
        report = stack.explainability
        self.assertIsInstance(report, ExplainabilityReport)
        self.assertGreaterEqual(len(report.selected), 2)
        self.assertGreaterEqual(len(report.rejected), 1)

        # Verify CLI output formatting
        cli_view = report.format_cli()
        self.assertIn("SELECTED SKILLS:", cli_view)
        self.assertIn("REJECTED CANDIDATES:", cli_view)

    def test_conflict_resolver(self):
        candidates = ["prisma-expert", "drizzle-orm-expert"]
        # Without preference, default priority is drizzle-orm-expert
        resolved, resolutions = self.conflict_resolver.resolve(candidates)
        self.assertEqual(resolved, ["drizzle-orm-expert"])
        self.assertEqual(len(resolutions), 1)
        self.assertEqual(resolutions[0]["winner"], "drizzle-orm-expert")
        self.assertEqual(resolutions[0]["loser"], "prisma-expert")

        # With explicit user preference for prisma
        resolved_pref, _ = self.conflict_resolver.resolve(
            candidates, user_preferences={"prisma"}
        )
        self.assertEqual(resolved_pref, ["prisma-expert"])

    def test_learning_engine_telemetry(self):
        rec = self.learning_engine.record_execution(
            task_id="test_run_001",
            query="test query",
            skills_used=["databases.postgresql", "design.frontend-design"],
            success=True,
            duration_ms=120.5,
            token_cost=1500,
            tool_calls=3,
        )
        self.assertTrue(rec.success)
        self.assertEqual(rec.task_id, "test_run_001")

        stats = self.learning_engine.get_skill_stats("databases.postgresql")
        self.assertGreaterEqual(stats["execution_count"], 1)
        self.assertGreaterEqual(stats["success_rate"], 0.9)


if __name__ == "__main__":
    unittest.main()
