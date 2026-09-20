"""Unit tests for SkillLoader."""

import unittest
from pathlib import Path
from core.skill_loader import SkillLoader


class TestSkillLoader(unittest.TestCase):
    def setUp(self):
        self.loader = SkillLoader()

    def test_scan_directory(self):
        skills = self.loader.scan_directory()
        self.assertIsInstance(skills, dict)


if __name__ == "__main__":
    unittest.main()
