"""Tests for the frontmatter parser."""
import sys
import unittest
from pathlib import Path

# Bootstrap sys.path so 'skills' resolves to src/skills (not tests/skill_tests/skills).
_ROOT = Path(__file__).resolve().parents[2]
_SRC = _ROOT / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))

from skills.frontmatter import parse_frontmatter, dump_frontmatter  # noqa: E402


class TestParseFrontmatter(unittest.TestCase):
    def test_basic(self):
        text = "---\nname: foo\ndescription: bar\n---\nbody"
        meta, body = parse_frontmatter(text)
        self.assertEqual(meta.get("name"), "foo")
        self.assertEqual(meta.get("description"), "bar")
        self.assertEqual(body.strip(), "body")

    def test_no_frontmatter(self):
        meta, body = parse_frontmatter("hello\nworld")
        self.assertEqual(meta, {})
        self.assertEqual(body, "hello\nworld")

    def test_list_value(self):
        text = "---\nname: x\ntriggers:\n  - one\n  - two\n---\nbody"
        meta, _ = parse_frontmatter(text)
        self.assertEqual(meta.get("triggers"), ["one", "two"])

    def test_inline_list(self):
        text = '---\nname: x\nkeywords: [a, b, "c d"]\n---\n'
        meta, _ = parse_frontmatter(text)
        self.assertEqual(meta.get("keywords"), ["a", "b", "c d"])

    def test_dump_roundtrip(self):
        meta = {"name": "foo", "aliases": ["x", "y"], "description": "test"}
        dumped = dump_frontmatter(meta)
        parsed, _ = parse_frontmatter(dumped + "\nbody")
        self.assertEqual(parsed["name"], "foo")
        self.assertEqual(parsed["aliases"], ["x", "y"])


if __name__ == "__main__":
    unittest.main()