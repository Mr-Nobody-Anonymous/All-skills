#!/usr/bin/env python3
"""Format and calculation verification test for health-economist skill."""
import re
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent

def test_icer_calculation_logic():
    # Verify mathematical correctness of ICER formula: ICER = (C1 - C0) / (E1 - E0)
    cost_base, effect_base = 28420.0, 7.12
    cost_int, effect_int = 33270.0, 7.50
    delta_c = cost_int - cost_base
    delta_e = effect_int - effect_base
    icer = delta_c / delta_e
    assert abs(delta_c - 4850.0) < 1e-4, f"Unexpected delta_c: {delta_c}"
    assert abs(delta_e - 0.38) < 1e-4, f"Unexpected delta_e: {delta_e}"
    assert abs(icer - 12763.1578) < 0.1, f"Unexpected ICER: {icer}"

def test_references_exist():
    ref_dir = SKILL_DIR / "references"
    assert ref_dir.exists(), "references/ directory must exist"
    required_refs = ["icer-calculations.md", "qaly-daly-framework.md", "cea-cua-guidelines.md"]
    for r in required_refs:
        p = ref_dir / r
        assert p.exists(), f"Missing reference file: {r}"

def test_examples_exist():
    ex_dir = SKILL_DIR / "examples"
    assert ex_dir.exists(), "examples/ directory must exist"
    assert (ex_dir / "good-cea-report.md").exists(), "Missing good-cea-report.md"
    assert (ex_dir / "bad-vs-good-economic-model.md").exists(), "Missing bad-vs-good-economic-model.md"

def test_skill_frontmatter():
    skill_md = SKILL_DIR / "SKILL.md"
    assert skill_md.exists(), "SKILL.md must exist"
    content = skill_md.read_text(encoding="utf-8")
    assert content.startswith("---"), "Must start with YAML frontmatter"
    assert "Use this skill when" in content, "Must include trigger guidelines"
    assert "Do not use this skill when" in content, "Must include negative trigger guidelines"

if __name__ == "__main__":
    test_icer_calculation_logic()
    test_references_exist()
    test_examples_exist()
    test_skill_frontmatter()
    print("health-economist tests passed successfully!")
