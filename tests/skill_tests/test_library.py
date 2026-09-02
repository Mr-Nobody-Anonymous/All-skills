"""End-to-end test: full library loads, routes, and validates."""
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.registry import load_registry  # noqa: E402
from skills.router import Router  # noqa: E402
from skills.validator import Validator  # noqa: E402


class TestLibraryE2E(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = load_registry(_ROOT)
        cls.router = Router(cls.reg)
        cls.validator = Validator(cls.reg, _ROOT / "skills")

    def test_minimum_skill_count(self):
        self.assertGreaterEqual(len(self.reg.entries), 50,
            msg=f"Expected >=50 skills, got {len(self.reg.entries)}")

    def test_all_categories_present(self):
        cats = set(self.reg.categories().keys())
        for required in {"productivity", "development", "research", "web", "documents", "design", "security", "utilities"}:
            self.assertIn(required, cats, f"Missing category: {required}")

    def test_validation_passes(self):
        result = self.validator.validate_all()
        self.assertEqual(len(result.errors), 0,
            msg=f"Validation errors: {result.errors}")

    def test_imported_skills_preserve_provenance(self):
        imported = [e for e in self.reg.entries if e.source not in {None, "custom"}]
        self.assertGreaterEqual(len(imported), 7)
        for entry in imported:
            skill_dir = _ROOT / "skills" / entry.path
            self.assertTrue((skill_dir / "LICENSE").is_file(), entry.id)
            self.assertTrue((skill_dir / "references" / "upstream-SKILL.md").is_file(), entry.id)

    def test_quarantine_is_not_registered(self):
        self.assertFalse(any("_quarantine" in e.path for e in self.reg.entries))

    def test_composition_targets_exist(self):
        for entry in self.reg.entries:
            for target in entry.composes_with + entry.suggests_after:
                self.assertIsNotNone(self.reg.get(target), f"{entry.id} -> {target}")


    def test_loader_rejects_quarantine_and_traversal(self):
        from skills.loader import Loader
        loader = Loader(_ROOT / "skills")
        self.assertIsNone(loader.resolve_path("_quarantine.suspicious"))
        self.assertIsNone(loader.resolve_path("development...secret"))
        self.assertIsNone(loader.resolve_path("../outside"))


    def test_router_top_queries(self):
        cases = {
            "I'm procrastinating": "productivity.unlazy",
            "help me focus": "productivity.focus",
            "review this code": "development.code-review",
            "break this into smaller tasks": "productivity.task-decomposition",
            "research this topic": "research.web-research",
            "check for security issues": "security.secure-coding",
            "write tests for this function": "development.testing",
            "make a presentation": "documents.pptx",
        }
        for q, expected in cases.items():
            m = self.router.route_one(q)
            self.assertIsNotNone(m, f"No match for: {q}")
            self.assertTrue(
                m.skill.id == expected or m.skill.id.startswith(expected.split(".")[0]),
                msg=f"Q: {q!r} expected {expected}, got {m.skill.id}",
            )


if __name__ == "__main__":
    unittest.main()