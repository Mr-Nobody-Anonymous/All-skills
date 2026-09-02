"""Tests for the router — natural language → skill ID mapping."""
import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.registry import Registry, SkillEntry  # noqa: E402
from skills.router import Router  # noqa: E402


def _entry(id_, name, description, **kw):
    return SkillEntry(
        id=id_, name=name, category=kw.get("category", id_.split(".", 1)[0]),
        description=description, path=id_.replace(".", "/"),
        aliases=kw.get("aliases", []), triggers=kw.get("triggers", []),
        keywords=kw.get("keywords", []),
        composes_with=kw.get("composes_with", []),
    )


class TestRouter(unittest.TestCase):
    def setUp(self):
        self.entries = [
            _entry("productivity.unlazy", "unlazy", "Help with procrastination",
                   triggers=["I'm procrastinating", "I can't get started", "help me start"],
                   keywords=["procrastinate", "lazy", "stuck", "avoid"]),
            _entry("productivity.focus", "focus", "Concentration and deep work",
                   triggers=["help me focus", "I can't concentrate"],
                   keywords=["focus", "concentrate", "distract"]),
            _entry("productivity.adhd", "adhd", "ADHD support",
                   triggers=["I have ADHD", "executive function"],
                   keywords=["adhd", "attention"]),
            _entry("productivity.task-decomposition", "task-decomposition", "Break down tasks",
                   triggers=["break this into smaller tasks", "decompose this"],
                   keywords=["break", "decompose", "subtasks", "steps"]),
            _entry("development.code-review", "code-review", "Review code",
                   triggers=["review this code", "code review"],
                   keywords=["review", "pr", "diff"]),
            _entry("development.testing", "testing", "Write tests",
                   triggers=["write tests for this"],
                   keywords=["test", "tdd", "unit"]),
            _entry("documents.pdf", "pdf", "Read PDFs",
                   keywords=["pdf", "document", "extract"]),
            _entry("documents.pptx", "pptx", "PowerPoint",
                   triggers=["make a presentation"],
                   keywords=["presentation", "slides", "deck"]),
            _entry("research.web-research", "web-research", "Research the web",
                   keywords=["research", "web", "search"]),
            _entry("security.secure-coding", "secure-coding", "Secure code",
                   keywords=["security", "owasp", "vulnerability"]),
        ]
        self.registry = Registry(entries=self.entries)
        self.router = Router(self.registry)

    def test_exact_id(self):
        m = self.router.route_one("productivity.unlazy")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "productivity.unlazy")
        self.assertEqual(m.matched_on, "id")

    def test_trigger_match(self):
        m = self.router.route_one("I'm procrastinating on my essay")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "productivity.unlazy")

    def test_focus(self):
        m = self.router.route_one("Help me focus for 30 minutes")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "productivity.focus")

    def test_adhd(self):
        m = self.router.route_one("I have ADHD and can't start")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "productivity.adhd")

    def test_break_down(self):
        m = self.router.route_one("Break this project into steps")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "productivity.task-decomposition")

    def test_code_review(self):
        m = self.router.route_one("Review this code")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "development.code-review")

    def test_testing(self):
        m = self.router.route_one("Write tests for this function")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "development.testing")

    def test_pdf(self):
        m = self.router.route_one("Analyze this PDF")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "documents.pdf")

    def test_presentation(self):
        m = self.router.route_one("Make a presentation")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "documents.pptx")

    def test_research(self):
        m = self.router.route_one("Research this topic")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "research.web-research")

    def test_security(self):
        m = self.router.route_one("Check for security issues")
        self.assertIsNotNone(m)
        self.assertEqual(m.skill.id, "security.secure-coding")

    def test_top_k(self):
        matches = self.router.route("Help me start working", top_k=3)
        self.assertGreaterEqual(len(matches), 1)
        self.assertLessEqual(len(matches), 3)
        self.assertIn(matches[0].skill.id, {"productivity.unlazy", "productivity.focus", "productivity.adhd"})

    def test_category_match(self):
        matches = self.router.route("productivity", top_k=10)
        self.assertTrue(matches)
        self.assertTrue(all(match.skill.category == "productivity" for match in matches))
        self.assertTrue(all(match.matched_on == "category" for match in matches))

    def test_route_chain_adds_composed_skill(self):
        source = self.registry.get("productivity.unlazy")
        source.composes_with = ["productivity.task-decomposition"]
        matches = self.router.route_chain("I'm procrastinating", top_k=5)
        self.assertIn("productivity.task-decomposition", [match.skill.id for match in matches])



if __name__ == "__main__":
    unittest.main()