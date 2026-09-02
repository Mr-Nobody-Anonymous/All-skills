"""Tests for the registry — loading, queries, and serialization."""
import sys
import tempfile
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.registry import Registry, SkillEntry, load_registry  # noqa: E402


def _write_skill(root: Path, category: str, name: str, **kwargs) -> Path:
    skill_dir = root / category / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    lines = ["---", f"name: {name}", f"category: {category}"]
    if kwargs.get("description"):
        lines.append(f"description: {kwargs['description']}")
    for k in ("aliases", "triggers", "keywords"):
        v = kwargs.get(k, [])
        if v:
            items = ", ".join(v)
            lines.append(f"{k}: [{items}]")
    if kwargs.get("source"):
        lines.append(f"source: {kwargs['source']}")
    lines.append("---")
    lines.append("")
    lines.append(f"# {name}\n\nbody")
    (skill_dir / "SKILL.md").write_text("\n".join(lines), encoding="utf-8")
    return skill_dir


class TestRegistryLoad(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.skills_root = self.tmp / "skills"
        # All skills live under skills_root
        _write_skill(self.skills_root, "productivity", "unlazy", description="help me start", triggers=["procrastinating"])
        _write_skill(self.skills_root, "development", "coding", description="write code", keywords=["implement", "function"])
        _write_skill(self.skills_root, "_quarantine", "bad", description="this should be ignored")

    def test_loads_enabled_skills(self):
        reg = Registry.load(self.skills_root / "registry.json", self.skills_root)
        ids = {e.id for e in reg.entries}
        self.assertIn("productivity.unlazy", ids)
        self.assertIn("development.coding", ids)
        self.assertNotIn("_quarantine.bad", ids)

    def test_categories(self):
        reg = Registry.load(self.skills_root / "registry.json", self.skills_root)
        cats = reg.categories()
        self.assertIn("productivity", cats)
        self.assertIn("development", cats)
        self.assertNotIn("_quarantine", cats)

    def test_search(self):
        reg = Registry.load(self.skills_root / "registry.json", self.skills_root)
        results = reg.search("procrastinating")
        ids = [r.id for r in results]
        self.assertIn("productivity.unlazy", ids)

    def test_get(self):
        reg = Registry.load(self.skills_root / "registry.json", self.skills_root)
        entry = reg.get("productivity.unlazy")
        self.assertIsNotNone(entry)
        self.assertEqual(entry.name, "unlazy")

    def test_to_json_roundtrip(self):
        reg = Registry.load(self.skills_root / "registry.json", self.skills_root)
        s = reg.to_json()
        self.assertIn("productivity.unlazy", s)
        self.assertIn("development.coding", s)


if __name__ == "__main__":
    unittest.main()