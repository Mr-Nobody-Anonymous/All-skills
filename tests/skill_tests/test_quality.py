"""Tests for quality scoring (P1 — prefer well-documented, low-risk skills)."""
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.quality import score_entry  # noqa: E402
from skills.registry import SkillEntry  # noqa: E402


def _entry(**kw):
    defaults = dict(
        id="productivity.unlazy", name="unlazy", category="productivity",
        description="A fairly complete skill description used for scoring checks.",
        path="productivity/unlazy", risk="low", version="1.0.0", source="custom",
    )
    defaults.update(kw)
    return SkillEntry(**defaults)


class TestQuality(unittest.TestCase):
    def test_rich_entry_scores_higher_than_sparse(self):
        rich = _entry(
            triggers=["help me start", "I can't get started"],
            keywords=["procrastinate", "lazy", "stuck", "avoid", "start"],
            capabilities=["start-task", "momentum"], inputs=["task"], outputs=["next-action"],
        )
        sparse = _entry(
            id="utilities.blank", name="blank", category="utilities", description="",
            path="utilities/blank", triggers=[], keywords=[], version="", source=None,
        )
        self.assertGreater(score_entry(rich).overall_score, score_entry(sparse).overall_score)

    def test_low_risk_scores_security_higher(self):
        low = _entry(risk="low")
        high = _entry(id="x.high", name="high", category="x", path="x/high", risk="high")
        self.assertGreater(score_entry(low).security, score_entry(high).security)

    def test_report_has_all_axes(self):
        report = score_entry(_entry())
        for axis in ("documentation", "maintenance", "reliability", "security", "compatibility", "usefulness"):
            self.assertIn(axis, report.to_dict())

    def test_overall_within_range(self):
        score = score_entry(_entry()).overall_score
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 10.0)


if __name__ == "__main__":
    unittest.main()