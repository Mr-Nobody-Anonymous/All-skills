"""Tests for the validator."""
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


def _write_skill(root, category, name, *, valid=True, with_evil=False):
    skill_dir = root / category / name
    skill_dir.mkdir(parents=True, exist_ok=True)
    if valid:
        body = (
            f"---\nname: {name}\ndescription: A complete test skill.\n"
            f"category: {category}\nversion: 1.0.0\n---\n\n# {name}\n\n"
            "## Purpose\nTest purpose.\n\n## When to Use\nUse in tests.\n\n"
            "## When NOT to Use\nDo not use outside tests.\n\n"
            "## Capabilities\n- Test validation.\n\n## Inputs\n- Test input.\n\n"
            "## Workflow\n1. Validate.\n\n## Tools\n- None.\n\n"
            "## Examples\nValidate this fixture.\n\n## Safety\nNo side effects.\n\n"
            "## Source\nTest fixture.\n\n## Notes\nCreated for validator tests.\n"
        )
        (skill_dir / "README.md").write_text(f"# {name}\n\nTest fixture.\n", encoding="utf-8")
    else:
        body = "# no frontmatter\n"
    if with_evil:
        body += "\nrm -rf / scary\n"
    (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")


class TestValidator(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.skills_root = self.tmp / "skills"
        _write_skill(self.skills_root, "productivity", "unlazy")
        _write_skill(self.skills_root, "development", "coding")
        _write_skill(self.skills_root, "productivity", "broken", valid=False)
        self.registry = Registry.load(
            self.skills_root / "registry.json",
            self.skills_root,
        )
        # Manually inject a registry entry for the broken one so validator sees it.
        self.registry.entries.append(
            SkillEntry(
                id="productivity.broken", name="broken", category="productivity",
                description="", path="productivity/broken",
            )
        )
        self.validator = Validator(self.registry, self.skills_root)

    def test_missing_frontmatter_caught(self):
        result = self.validator.validate_one("productivity.broken")
        self.assertFalse(result.ok)

    def test_missing_path_caught(self):
        result = self.validator.validate_one("productivity.nonexistent")
        self.assertFalse(result.ok)

    def test_valid_skill(self):
        result = self.validator.validate_one("productivity.unlazy")
        self.assertEqual(len(result.errors), 0)


    def test_process_env_is_not_a_credential_file_warning(self):
        skill_dir = self.skills_root / "productivity" / "unlazy"
        (skill_dir / "example.js").write_text("const key = process.env.EXAMPLE_API_KEY;", encoding="utf-8")
        result = self.validator.validate_one("productivity.unlazy")
        self.assertFalse(any("credential file" in warning for warning in result.warnings))


if __name__ == "__main__":
    unittest.main()