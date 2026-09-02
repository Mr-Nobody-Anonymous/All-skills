"""Tests that exercise the live skills/registry.json — not a synthetic registry.

These tests verify the master prompt §18 routing scenarios against the
real installed skills.
"""
import json
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.registry import load_registry  # noqa: E402
from skills.router import Router  # noqa: E402


class TestLiveRegistry(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reg = load_registry(_ROOT)
        cls.router = Router(cls.reg)
        cls.ids = {e.id for e in cls.reg.entries}

    def _route_top(self, query):
        m = self.router.route_one(query)
        self.assertIsNotNone(m, f"no match for: {query!r}")
        return m

    # Master prompt §18 routing scenarios -------------------------------

    def test_procrastination_routes_to_unlazy(self):
        m = self._route_top("I'm procrastinating on my programming assignment.")
        self.assertEqual(m.skill.id, "productivity.unlazy")

    def test_focus_session(self):
        m = self._route_top("Help me focus for the next 30 minutes.")
        self.assertEqual(m.skill.id, "productivity.focus")

    def test_break_down_routes_to_task_decomposition(self):
        m = self._route_top("Break my project into smaller tasks.")
        self.assertEqual(m.skill.id, "productivity.task-decomposition")

    def test_code_review(self):
        m = self._route_top("Review this Python code for security problems.")
        self.assertEqual(m.skill.id, "development.code-review")

    def test_security_check(self):
        m = self._route_top("Check this code for security issues.")
        self.assertEqual(m.skill.id, "security.secure-coding")

    def test_research_topic(self):
        m = self._route_top("Research this topic.")
        self.assertEqual(m.skill.id, "research.web-research")

    def test_pdf(self):
        m = self._route_top("Analyze this PDF.")
        self.assertEqual(m.skill.id, "documents.pdf")

    # Master prompt §15 "doctor" requirement -----------------------------

    def test_50_plus_skills(self):
        self.assertGreaterEqual(
            len(self.reg.entries), 50,
            f"expected at least 50 skills, found {len(self.reg.entries)}",
        )

    def test_eight_categories(self):
        cats = set(self.reg.categories())
        for required in {
            "productivity", "development", "research", "web",
            "documents", "design", "security", "utilities",
        }:
            self.assertIn(required, cats, f"missing category: {required}")

    def test_every_skill_has_required_frontmatter(self):
        for e in self.reg.entries:
            self.assertTrue(e.name, f"{e.id} missing name")
            self.assertTrue(e.description, f"{e.id} missing description")
            self.assertTrue(e.path, f"{e.id} missing path")
            skill_md = _ROOT / "skills" / Path(*e.path.split("/")) / "SKILL.md"
            self.assertTrue(skill_md.exists(), f"{e.id} missing SKILL.md at {skill_md}")

    def test_every_skill_id_is_unique(self):
        ids = [e.id for e in self.reg.entries]
        self.assertEqual(len(ids), len(set(ids)), "duplicate skill ids")

    def test_no_enabled_is_false(self):
        for e in self.reg.entries:
            self.assertTrue(e.enabled, f"{e.id} should be enabled by default")


class TestAuxiliaryFiles(unittest.TestCase):
    """Master prompt §8 / §14 / §17 / §20 require several auxiliary files."""

    def test_registry_json(self):
        self.assertTrue((_ROOT / "skills" / "registry.json").exists())
        data = json.loads((_ROOT / "skills" / "registry.json").read_text(encoding="utf-8"))
        self.assertIn("skills", data)
        self.assertGreaterEqual(len(data["skills"]), 50)

    def test_registry_md(self):
        p = _ROOT / "skills" / "registry.md"
        self.assertTrue(p.exists(), "skills/registry.md missing (master prompt §8)")
        text = p.read_text(encoding="utf-8")
        self.assertIn("Skill Registry", text)
        self.assertIn("Total skills", text)

    def test_sources_json(self):
        p = _ROOT / "skills" / "SOURCES.json"
        self.assertTrue(p.exists(), "skills/SOURCES.json missing (master prompt §20)")
        data = json.loads(p.read_text(encoding="utf-8"))
        self.assertIn("skills", data)
        self.assertGreaterEqual(len(data["skills"]), 50)

    def test_dependencies_md(self):
        p = _ROOT / "skills" / "DEPENDENCIES.md"
        self.assertTrue(p.exists(), "skills/DEPENDENCIES.md missing (master prompt §14)")
        text = p.read_text(encoding="utf-8")
        self.assertIn("Skill Dependencies", text)
        self.assertIn("Per-Skill Status", text)

    def test_quarantine_dir(self):
        self.assertTrue((_ROOT / "skills" / "_quarantine").exists(),
                        "skills/_quarantine missing (master prompt §13)")

    def test_docs_skills_security(self):
        p = _ROOT / "docs" / "skills" / "SECURITY.md"
        self.assertTrue(p.exists(), "docs/skills/SECURITY.md missing")
        text = p.read_text(encoding="utf-8").lower()
        for required in ("threat model", "quarantine", "validator", "permissions"):
            self.assertIn(required, text, f"SECURITY.md missing section: {required}")

    def test_per_category_docs(self):
        # SECURITY.md (uppercase) is the hand-written policy file. The
        # per-category doc for `security` lives at `security-category.md` so
        # it does not collide with the policy file on case-sensitive
        # filesystems.
        docs_dir = _ROOT / "docs" / "skills"
        for cat, filename in (
            ("productivity", "productivity.md"),
            ("development", "development.md"),
            ("research", "research.md"),
            ("web", "web.md"),
            ("documents", "documents.md"),
            ("design", "design.md"),
            ("security", "security-category.md"),
            ("utilities", "utilities.md"),
        ):
            with self.subTest(category=cat):
                p = docs_dir / filename
                self.assertTrue(p.exists(), f"docs/skills/{filename} missing")
                text = p.read_text(encoding="utf-8")
                self.assertIn(f"{cat.title()} Skills", text)


if __name__ == "__main__":
    unittest.main()
