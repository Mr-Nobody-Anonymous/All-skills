"""Declared execution contracts must agree with a skill's tools and instructions."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.contracts import check_contract  # noqa: E402
from skills.frontmatter import parse_frontmatter  # noqa: E402

FIXING_BODY = "## Workflow\n1. Reproduce the failure.\n2. **Add a regression test.**\n3. Fix the code.\n"


class TestContractChecks(unittest.TestCase):
    def test_write_tools_require_write_access(self):
        issues = check_contract({"tools": ["file_read", "file_write"], "filesystem_access": "read"}, "")
        self.assertEqual([i.field for i in issues], ["filesystem_access"])
        self.assertEqual(check_contract({"tools": ["file_write"], "filesystem_access": "write"}, ""), [])

    def test_instructions_that_modify_files_require_write_access(self):
        issues = check_contract({"filesystem_access": "read"}, FIXING_BODY)
        self.assertEqual(len(issues), 1)
        self.assertIn("Add a regression test", issues[0].message)
        self.assertEqual(check_contract({"filesystem_access": "write"}, FIXING_BODY), [])

    def test_advisory_skills_may_recommend_changes(self):
        meta = {"filesystem_access": "read", "execution_mode": "advisory"}
        self.assertEqual(check_contract(meta, FIXING_BODY), [])

    def test_code_examples_and_prose_are_not_instructions(self):
        body = "## Notes\nA fix is only done when tests exist.\n```bash\ngit commit -m 'fix the code'\n```\n"
        self.assertEqual(check_contract({"filesystem_access": "read"}, body), [])

    def test_network_tools_require_network_access(self):
        issues = check_contract({"tools": ["read_url"], "network_access": False}, "")
        self.assertEqual([i.field for i in issues], ["network_access"])

    def test_debugging_skill_declares_what_it_does(self):
        """The review's example: debugging fixes code and adds tests, so it must declare write access."""
        meta, body = parse_frontmatter((_ROOT / "skills" / "development" / "debugging" / "SKILL.md").read_text(encoding="utf-8"))
        self.assertEqual(meta["filesystem_access"], "write")
        self.assertEqual(check_contract(meta, body), [])

    def test_library_contracts_are_consistent(self):
        files = sorted((_ROOT / "skills").glob("*/*/SKILL.md")) + sorted((_ROOT / ".agents" / "skills").glob("*/SKILL.md"))
        broken = []
        for path in files:
            meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
            broken += [f"{path.parent.relative_to(_ROOT)}: {i.message}" for i in check_contract(meta, body)]
        self.assertEqual(broken, [], broken[:3])


if __name__ == "__main__":
    unittest.main()
