"""Tests for declared skill-conflict detection (P1)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.registry import Registry, SkillEntry  # noqa: E402
from skills.validator import Validator  # noqa: E402


class TestConflicts(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.skills_root = self.tmp / "skills"
        self.skills_root.mkdir(parents=True, exist_ok=True)
        (self.skills_root / "conflicts.json").write_text(json.dumps({
            "conflicts": [
                {"skills": ["productivity.a", "utilities.b"], "severity": "error",
                 "reason": "both cannot be enabled"},
                {"skills": ["productivity.a", "missing.skill"], "severity": "warn",
                 "reason": "references unknown skill"},
            ]
        }), encoding="utf-8")
        self.registry = Registry(entries=[
            SkillEntry(id="productivity.a", name="a", category="productivity",
                       description="d", path="productivity/a", enabled=True),
            SkillEntry(id="utilities.b", name="b", category="utilities",
                       description="d", path="utilities/b", enabled=True),
        ])
        self.validator = Validator(self.registry, self.skills_root)

    def test_active_conflict_reported(self):
        result = self.validator.validate_all()
        self.assertTrue(any("active conflict" in e for e in result.errors))

    def test_unknown_skill_reported(self):
        result = self.validator.validate_all()
        self.assertTrue(any("unknown skill" in e for e in result.errors))


if __name__ == "__main__":
    unittest.main()