#!/usr/bin/env python3
"""Skill Benchmark Evaluation Harness.

Evaluates skills against an 8-dimension quality rubric:
1. Frontmatter Schema Completeness
2. Invocation Rules & Triggers
3. Inputs & Outputs Contract
4. Workflow Granularity & Steps
5. Practical Examples
6. Safety & Sandboxing Boundaries
7. Fallback & Recovery Specification
8. Token Economy & Conciseness

Usage:
    python scripts/benchmark_skills.py
    python scripts/benchmark_skills.py --skill active.tdd
    python scripts/benchmark_skills.py --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.frontmatter import parse_frontmatter
from skills.registry import load_registry


def evaluate_skill(name: str, text: str, meta: dict) -> dict:
    scores = {}

    # 1. Frontmatter Completeness (0-10)
    fm_keys = ["name", "description", "category", "version", "triggers", "keywords", "tools", "recovery"]
    fm_present = sum(1 for k in fm_keys if k in meta and meta[k])
    scores["frontmatter"] = round((fm_present / len(fm_keys)) * 10, 1)

    # 2. Invocation Rules (0-10)
    scores["invocation"] = 10.0 if "disable-model-invocation" in meta else 5.0

    # 3. Inputs & Outputs (0-10)
    has_inputs = bool(re.search(r"##\s+(Inputs|Parameters)", text, re.I))
    has_outputs = bool(re.search(r"##\s+Outputs", text, re.I))
    scores["contracts"] = 10.0 if (has_inputs and has_outputs) else 5.0 if (has_inputs or has_outputs) else 2.0

    # 4. Workflow Steps (0-10)
    has_workflow = bool(re.search(r"##\s+Workflow", text, re.I))
    has_steps = len(re.findall(r"(?:###?\s+Step|\d+\.\s+\*\*Phase)", text)) >= 2
    scores["workflow"] = 10.0 if (has_workflow and has_steps) else 7.0 if has_workflow else 3.0

    # 5. Practical Examples (0-10)
    has_examples = bool(re.search(r"##\s+Examples?", text, re.I))
    has_prompts = bool(re.search(r"(?:User Prompt|User Request|Example \d)", text, re.I))
    scores["examples"] = 10.0 if (has_examples and has_prompts) else 6.0 if has_examples else 2.0

    # 6. Safety & Boundaries (0-10)
    has_safety = bool(re.search(r"##\s+Safety", text, re.I))
    has_boundaries = bool(re.search(r"(?:forbidden|destructive|guardrail|blocklist)", text, re.I))
    scores["safety"] = 10.0 if (has_safety and has_boundaries) else 7.0 if (has_safety or has_boundaries) else 4.0

    # 7. Fallback & Recovery (0-10)
    has_recovery_fm = "recovery" in meta
    has_recovery_text = bool(re.search(r"(?:fallback|recovery|loop|retry)", text, re.I))
    scores["recovery"] = 10.0 if (has_recovery_fm and has_recovery_text) else 6.0 if (has_recovery_fm or has_recovery_text) else 2.0

    # 8. Token Economy (0-10)
    char_len = len(text)
    scores["token_economy"] = 10.0 if (800 <= char_len <= 8000) else 7.0 if char_len < 15000 else 4.0

    overall = round(sum(scores.values()) / len(scores), 1)
    return {
        "skill": name,
        "overall_score": overall,
        "dimensions": scores,
        "char_count": char_len
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Skill Benchmark Evaluation Harness")
    parser.add_argument("--skill", default="", help="Evaluate a single skill")
    parser.add_argument("--json", action="store_true", help="Output benchmark results as JSON")
    args = parser.parse_args()

    active_dir = REPO_ROOT / ".agents" / "skills"
    results = []

    for skill_dir in sorted(active_dir.iterdir()):
        if not skill_dir.is_dir():
            continue
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
        if args.skill and args.skill not in (skill_dir.name, f"active.{skill_dir.name}"):
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")
        meta, _ = parse_frontmatter(text)
        res = evaluate_skill(skill_dir.name, text, meta)
        results.append(res)

    if args.json:
        print(json.dumps(results, indent=2))
        return 0

    print("=" * 70)
    print("📊 ALL SKILLS — 8-DIMENSION QUALITY BENCHMARK REPORT")
    print("=" * 70)
    print(f"{'Skill Name':<35} {'Score':<8} {'FM':<5} {'Invoc':<6} {'Steps':<6} {'Safety':<6}")
    print("-" * 70)

    for r in results[:25]:
        d = r["dimensions"]
        print(f"{r['skill']:<35} {r['overall_score']:<8} {d['frontmatter']:<5} {d['invocation']:<6} {d['workflow']:<6} {d['safety']:<6}")

    if len(results) > 25:
        print(f"... and {len(results) - 25} more skills benchmarked.")

    avg_score = round(sum(r["overall_score"] for r in results) / len(results), 1) if results else 0
    print("-" * 70)
    print(f"Total Skills Benchmarked: {len(results)} | Average Score: {avg_score} / 10.0")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
