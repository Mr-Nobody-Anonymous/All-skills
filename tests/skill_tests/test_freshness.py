"""Deterministic coverage for freshness tiers, drift warnings and library helpers."""
from __future__ import annotations

import datetime
import os
import tempfile
import unittest
from pathlib import Path

from skills.freshness import FreshnessEngine
from skills.library import discover, load, route, route_chain
from skills.registry import Registry, SkillEntry

ROOT = Path(__file__).resolve().parents[2]
REFERENCE_DATE = datetime.date(2026, 10, 4)


def _entry(skill_id: str = "utilities.demo", path: str = "utilities/demo") -> SkillEntry:
    return SkillEntry(
        id=skill_id,
        name=skill_id.rsplit(".", 1)[-1],
        category=skill_id.split(".", 1)[0],
        description="A sample skill used to validate freshness behavior.",
        path=path,
    )


class TestFreshnessEngine(unittest.TestCase):
    def test_default_verification_date_and_fresh_tier(self):
        report = FreshnessEngine().assess_skill(_entry(), reference_date=REFERENCE_DATE)
        self.assertEqual(report.last_verified_date, "2026-09-20")
        self.assertEqual(report.tier, "fresh")
        self.assertFalse(report.drift_detected)
        self.assertEqual(report.to_dict()["skill_id"], "utilities.demo")

    def test_all_age_tiers_and_future_dates(self):
        engine = FreshnessEngine()
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp)
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text("Current guidance.", encoding="utf-8")
            for days, expected in ((0, "fresh"), (30, "stable"), (91, "aging"), (181, "stale"), (-5, "fresh")):
                with self.subTest(days=days):
                    verified_date = REFERENCE_DATE - datetime.timedelta(days=days)
                    timestamp = datetime.datetime.combine(verified_date, datetime.time.min).timestamp()
                    os.utime(skill_file, (timestamp, timestamp))
                    report = engine.assess_skill(
                        _entry(), skill_dir=skill_dir, reference_date=REFERENCE_DATE
                    )
                    self.assertEqual(report.tier, expected)
                    self.assertGreaterEqual(report.days_since_update, 0)

    def test_skill_file_mtime_and_legacy_drift_reduce_score(self):
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "utilities" / "demo"
            skill_dir.mkdir(parents=True)
            skill_file = skill_dir / "SKILL.md"
            skill_file.write_text("Use var value = 1; componentWillMount()", encoding="utf-8")
            timestamp = datetime.datetime.combine(
                REFERENCE_DATE - datetime.timedelta(days=100), datetime.time.min
            ).timestamp()
            os.utime(skill_file, (timestamp, timestamp))

            report = FreshnessEngine().assess_skill(
                _entry(), skill_dir=skill_dir, reference_date=REFERENCE_DATE
            )
            self.assertEqual(report.tier, "aging")
            self.assertTrue(report.drift_detected)
            self.assertEqual(len(report.drift_warnings), 2)

    def test_assess_all_resolves_registry_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            skills_root = Path(tmp) / "skills"
            skill_dir = skills_root / "utilities" / "demo"
            skill_dir.mkdir(parents=True)
            (skill_dir / "SKILL.md").write_text("Modern skill guidance.", encoding="utf-8")
            entry = _entry()
            reports = FreshnessEngine().assess_all(Registry([entry]), skills_root)
            self.assertIn(entry.id, reports)
            self.assertFalse(reports[entry.id].drift_detected)


class TestLibraryHelpers(unittest.TestCase):
    def test_programmatic_helpers_discover_route_chain_and_load(self):
        registry = discover(ROOT)
        self.assertGreater(len(registry.entries), 0)
        self.assertTrue(route("how to build an embedding search", ROOT, top_k=1))
        self.assertTrue(route_chain("review and improve code", ROOT, top_k=3))
        self.assertIsNotNone(load("ai.embeddings", ROOT))


if __name__ == "__main__":
    unittest.main()
