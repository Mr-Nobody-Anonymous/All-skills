#!/usr/bin/env python3
"""Format and integrity test for architecture-decision-records skill."""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

def test_adr_templates_exist():
    templates_dir = SKILL_DIR / "templates"
    assert templates_dir.exists(), "templates/ directory must exist"
    required_templates = ["madr-template.md", "nygard-template.md", "lightweight-template.md", "deprecation-template.md"]
    for t in required_templates:
        p = templates_dir / t
        assert p.exists(), f"Missing template: {t}"
        content = p.read_text(encoding="utf-8")
        assert "Status" in content or "status" in content, f"Template {t} missing status heading"

def test_adr_examples_exist():
    examples_dir = SKILL_DIR / "examples"
    assert examples_dir.exists(), "examples/ directory must exist"
    assert (examples_dir / "good-adr-example.md").exists(), "Missing good-adr-example.md"
    assert (examples_dir / "bad-adr-example.md").exists(), "Missing bad-adr-example.md"

def test_skill_markdown_structure():
    skill_md = SKILL_DIR / "SKILL.md"
    assert skill_md.exists(), "SKILL.md must exist"
    content = skill_md.read_text(encoding="utf-8")
    assert content.startswith("---"), "Must start with YAML frontmatter"
    assert "Use this skill when" in content, "Must include positive trigger guidance"
    assert "Do not use this skill when" in content, "Must include negative trigger guidance"
    assert "Security & Sandboxing Boundaries" in content, "Must include security boundaries"

if __name__ == "__main__":
    test_adr_templates_exist()
    test_adr_examples_exist()
    test_skill_markdown_structure()
    print("architecture-decision-records tests passed successfully!")
