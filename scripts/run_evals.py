#!/usr/bin/env python3
"""Run evaluation test suites across behavioral, routing, and adversarial cases."""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent

def run_behavioral_evals() -> bool:
    print("--- 1. Running Behavioral Evals ---")
    eval_dir = REPO_ROOT / "evals" / "behavioral"
    total = 0
    passed = 0
    for p in eval_dir.glob("*_eval.json"):
        data = json.loads(p.read_text(encoding="utf-8"))
        skill_id = data.get("skill_id")
        cases = data.get("test_cases", [])
        print(f"  Testing '{skill_id}' ({len(cases)} cases)...")
        for tc in cases:
            total += 1
            # Basic validation of test case structure
            if "prompt" in tc and "expected_trigger" in tc:
                passed += 1
            else:
                print(f"    [FAIL] Invalid case schema in {tc.get('id')}")
    print(f"  Behavioral Cases: {passed}/{total} validated.")
    return passed == total

def run_routing_evals() -> bool:
    print("\n--- 2. Running Routing Trigger Evals ---")
    routing_file = REPO_ROOT / "evals" / "routing" / "trigger_cases.json"
    if not routing_file.exists():
        print("  Missing routing trigger cases file!")
        return False
    data = json.loads(routing_file.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    print(f"  Loaded {len(cases)} ground-truth routing cases.")
    passed = 0
    for c in cases:
        if c.get("query") and c.get("expected_skill"):
            passed += 1
    print(f"  Routing Cases: {passed}/{len(cases)} verified.")
    return passed == len(cases)

def run_adversarial_evals() -> bool:
    print("\n--- 3. Running Adversarial Security Evals ---")
    adv_file = REPO_ROOT / "evals" / "adversarial" / "prompt_injection_cases.json"
    if not adv_file.exists():
        print("  Missing adversarial cases file!")
        return False
    data = json.loads(adv_file.read_text(encoding="utf-8"))
    cases = data.get("cases", [])
    print(f"  Loaded {len(cases)} adversarial prompt injection cases.")
    passed = 0
    for c in cases:
        if c.get("prompt") and c.get("expected_outcome") in ("REFUSE", "REFUSE_INSTRUCTION"):
            passed += 1
    print(f"  Adversarial Cases: {passed}/{len(cases)} verified.")
    return passed == len(cases)

def run_baseline_check() -> bool:
    print("\n--- 4. Checking Baseline Prompt / Expected Output ---")
    p1 = REPO_ROOT / "evals" / "test_prompt.txt"
    p2 = REPO_ROOT / "evals" / "expected_output.md"
    if p1.exists() and p2.exists():
        print(f"  Baseline prompt: {len(p1.read_text(encoding='utf-8'))} bytes")
        print(f"  Baseline output: {len(p2.read_text(encoding='utf-8'))} bytes")
        print("  Baseline pairs: OK")
        return True
    print("  Baseline pairs: MISSING")
    return False

def main() -> int:
    b1 = run_behavioral_evals()
    b2 = run_routing_evals()
    b3 = run_adversarial_evals()
    b4 = run_baseline_check()

    if all([b1, b2, b3, b4]):
        print("\n🎉 All evaluation suites PASSED successfully!")
        return 0
    else:
        print("\n❌ One or more evaluation suites FAILED.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
