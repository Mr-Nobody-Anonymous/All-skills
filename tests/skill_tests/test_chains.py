"""Tests for named skill chains (P1 — deterministic workflows in chains.json)."""
import json
import sys
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.chains import ChainResolver, ChainStore  # noqa: E402
from skills.registry import Registry, SkillEntry  # noqa: E402

CHAIN = {
    "chains": [
        {
            "name": "deep-research",
            "description": "research workflow",
            "steps": ["research.web-research", "research.fact-checking"],
            "inputs": ["topic"],
            "outputs": ["report.md"],
        }
    ]
}


class TestChains(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.path = self.tmp / "chains.json"
        self.path.write_text(json.dumps(CHAIN), encoding="utf-8")
        self.store = ChainStore.load(self.path)

    def test_load_and_get(self):
        chain = self.store.get("deep-research")
        self.assertIsNotNone(chain)
        self.assertEqual(chain.steps, ["research.web-research", "research.fact-checking"])
        self.assertEqual(chain.inputs, ["topic"])

    def test_missing_chain(self):
        self.assertIsNone(self.store.get("nope"))

    def test_names(self):
        self.assertEqual(self.store.names(), ["deep-research"])

    def test_resolve_existing(self):
        reg = Registry(entries=[
            SkillEntry(id="research.web-research", name="web-research", category="research",
                       description="web", path="research/web-research"),
            SkillEntry(id="research.fact-checking", name="fact-checking", category="research",
                       description="facts", path="research/fact-checking"),
        ])
        resolver = ChainResolver(reg)
        plan = self.store.get("deep-research")
        self.assertEqual(resolver.unresolved_steps(plan), [])
        self.assertEqual(len(resolver.resolve(plan)), 2)

    def test_resolve_missing(self):
        resolver = ChainResolver(Registry(entries=[]))
        plan = self.store.get("deep-research")
        self.assertEqual(len(resolver.unresolved_steps(plan)), 2)


if __name__ == "__main__":
    unittest.main()