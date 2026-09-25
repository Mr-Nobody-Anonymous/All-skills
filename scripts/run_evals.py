#!/usr/bin/env python3
"""Run the evaluation suites against the real router, scanner and policy engine.

Each suite executes the behaviour under test and compares observed results
with the expectations in ``evals/`` — a case passes only if the behaviour
matches, never merely because its fixture has the right fields.

1. Behavioral   ``evals/behavioral/*_eval.json``: the prompt must (or must not)
                route to the skill, and the skill's instructions must cover the
                required output sections and avoid forbidden content.
2. Routing      ``evals/routing/trigger_cases.json``: the expected skill must be
                among the router's top 3 (top-1 accuracy is reported too).
3. Adversarial  ``evals/adversarial/prompt_injection_cases.json``: every attack
                must be refused by the router's safety gate.
4. Security     ``evals/security/security_cases.json``: BLOCKED / APPROVAL_REQUIRED
                verdicts from the safety gate and the policy engine.
5. OOD          ``evals/routing/ood_cases.json``: out-of-domain queries must not
                activate a skill (>= 95% rejection).
6. Baseline     ``evals/test_prompt.txt`` must route to the ADR skill and
                ``evals/expected_output.md`` must satisfy that skill's contract.
"""
from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.policy import PolicyEngine, PolicyVerdict  # noqa: E402
from skills.registry import load_registry  # noqa: E402
from skills.router import ConfidenceLevel, Router  # noqa: E402

TRIGGER_MIN_SCORE = 20.0   # router confidence needed to count as "triggered"
ROUTING_MIN_TOP3 = 0.90    # required top-3 routing accuracy
OOD_MIN_REJECTION = 95.0


@lru_cache(maxsize=1)
def _router() -> Router:
    return Router(load_registry(REPO_ROOT), workspace_root=REPO_ROOT)


def _load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _skill_text(skill_name: str) -> str:
    """All markdown instructions/templates of a skill (canonical or active harness)."""
    folders = sorted(REPO_ROOT.glob(f"skills/*/{skill_name}")) or [REPO_ROOT / ".agents" / "skills" / skill_name]
    folder = folders[0]
    return "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in sorted(folder.rglob("*.md"))).lower()


def _top_names(query: str, k: int = 3) -> List[str]:
    return [m.skill.name for m in _router().route(query, top_k=k)]


def _triggered(query: str, skill_name: str) -> bool:
    decision = _router().route_with_confidence(query, min_confidence=TRIGGER_MIN_SCORE)
    selected = decision.selected_skill
    return selected is not None and selected.rsplit(".", 1)[-1] == skill_name


def run_behavioral_evals(suites: Optional[List[Dict[str, Any]]] = None) -> bool:
    print("--- 1. Behavioral evals (routing trigger + instruction contract) ---")
    if suites is None:
        suites = [_load(p) for p in sorted((REPO_ROOT / "evals" / "behavioral").glob("*_eval.json"))]
    total = passed = 0
    for suite in suites:
        skill = suite["skill_id"]
        text = _skill_text(skill)
        for tc in suite.get("test_cases", []):
            total += 1
            problems = []
            if _triggered(tc["prompt"], skill) != bool(tc["expected_trigger"]):
                top = _top_names(tc["prompt"], 1)
                problems.append(f"expected_trigger={tc['expected_trigger']} but router chose {top[:1] or 'nothing'}")
            if tc["expected_trigger"]:
                missing = [sec for sec in tc.get("required_sections", []) if sec.lower() not in text]
                if missing:
                    problems.append(f"skill instructions do not cover sections {missing}")
                present = [kw for kw in tc.get("forbidden_keywords", []) if kw.lower() in text]
                if present:
                    problems.append(f"skill contains forbidden content {present}")
            if problems:
                print(f"    [FAIL] {tc.get('id')}: {'; '.join(problems)}")
            else:
                passed += 1
    print(f"  Behavioral cases: {passed}/{total} passed.")
    return total > 0 and passed == total


def run_routing_evals(cases: Optional[List[Dict[str, Any]]] = None) -> bool:
    print("\n--- 2. Routing evals (expected skill in router top-3) ---")
    if cases is None:
        cases = _load(REPO_ROOT / "evals" / "routing" / "trigger_cases.json")["cases"]
    indexed = {e.name for e in _router().registry.entries}
    not_indexed = [c for c in cases if c["expected_skill"] not in indexed]
    cases = [c for c in cases if c["expected_skill"] in indexed]
    if not_indexed:
        print(f"  {len(not_indexed)} case(s) target skills the canonical router does not index "
              f"(active-harness skills) and are NOT evaluated: "
              f"{', '.join(sorted({c['expected_skill'] for c in not_indexed}))}")
    top1 = top3 = 0
    for c in cases:
        names = _top_names(c["query"], 3)
        top1 += bool(names) and names[0] == c["expected_skill"]
        if c["expected_skill"] in names:
            top3 += 1
        else:
            print(f"    [MISS] {c.get('id')}: expected {c['expected_skill']}, got {names}")
    acc3 = top3 / len(cases) if cases else 0.0
    print(f"  Top-1 accuracy: {top1}/{len(cases)}   Top-3 accuracy: {top3}/{len(cases)} ({acc3:.0%}, "
          f"required {ROUTING_MIN_TOP3:.0%})")
    return bool(cases) and acc3 >= ROUTING_MIN_TOP3


def run_adversarial_evals(cases: Optional[List[Dict[str, Any]]] = None) -> bool:
    print("\n--- 3. Adversarial evals (attacks must be refused) ---")
    if cases is None:
        cases = _load(REPO_ROOT / "evals" / "adversarial" / "prompt_injection_cases.json")["cases"]
    passed = 0
    for c in cases:
        decision = _router().route_with_confidence(c["prompt"])
        refused = decision.confidence_level == ConfidenceLevel.UNSAFE
        expected_refusal = c.get("expected_outcome") in ("REFUSE", "REFUSE_INSTRUCTION")
        if refused == expected_refusal:
            passed += 1
        else:
            chosen = decision.selected_skill.id if decision.selected_skill else "no skill"
            print(f"    [FAIL] {c.get('id')} ({c.get('attack_type')}): router returned "
                  f"{decision.confidence_level.value} / {chosen}")
    print(f"  Adversarial cases: {passed}/{len(cases)} handled as expected.")
    return bool(cases) and passed == len(cases)


def run_security_evals(cases: Optional[List[Dict[str, Any]]] = None) -> bool:
    print("\n--- 4. Security policy evals (BLOCKED / APPROVAL_REQUIRED) ---")
    if cases is None:
        cases = _load(REPO_ROOT / "evals" / "security" / "security_cases.json")
    engine = PolicyEngine(REPO_ROOT)
    passed = 0
    for c in cases:
        unsafe = _router().route_with_confidence(c["prompt"]).confidence_level == ConfidenceLevel.UNSAFE
        verdict = engine.evaluate_request(c["prompt"]).overall_verdict
        observed = ("BLOCKED" if unsafe or verdict == PolicyVerdict.DENY
                    else "APPROVAL_REQUIRED" if verdict == PolicyVerdict.ASK else "ALLOWED")
        if observed == c["expected_verdict"]:
            passed += 1
        else:
            print(f"    [FAIL] {c['prompt'][:60]!r}: expected {c['expected_verdict']}, observed {observed}")
    print(f"  Security cases: {passed}/{len(cases)} passed.")
    return bool(cases) and passed == len(cases)


def run_ood_evals(cases: Optional[List[Dict[str, Any]]] = None) -> bool:
    print("\n--- 5. Out-of-distribution evals ---")
    if cases is None:
        cases = _load(REPO_ROOT / "evals" / "routing" / "ood_cases.json")
    rejected = 0
    for c in cases:
        match = _router().route_one(c.get("query", ""))
        if match is None or match.score < 40.0:
            rejected += 1
    rate = (rejected / len(cases)) * 100.0 if cases else 0.0
    print(f"  OOD rejection rate: {rate:.1f}% ({rejected}/{len(cases)}), required {OOD_MIN_REJECTION:.0f}%")
    return bool(cases) and rate >= OOD_MIN_REJECTION


def run_baseline_check() -> bool:
    print("\n--- 6. Baseline prompt / expected output ---")
    prompt = (REPO_ROOT / "evals" / "test_prompt.txt").read_text(encoding="utf-8")
    expected = (REPO_ROOT / "evals" / "expected_output.md").read_text(encoding="utf-8").lower()
    suite = _load(REPO_ROOT / "evals" / "behavioral" / "adr_eval.json")
    required = suite["test_cases"][0].get("required_sections", [])
    routed = _triggered(prompt, suite["skill_id"])
    missing = [sec for sec in required if sec.lower() not in expected]
    print(f"  Baseline prompt routes to {suite['skill_id']}: {'yes' if routed else 'NO'}")
    print(f"  Expected output covers required sections: {'yes' if not missing else f'NO, missing {missing}'}")
    return routed and not missing


def main() -> int:
    results = [
        run_behavioral_evals(),
        run_routing_evals(),
        run_adversarial_evals(),
        run_security_evals(),
        run_ood_evals(),
        run_baseline_check(),
    ]
    if all(results):
        print(f"\n🎉 All {len(results)} evaluation suites PASSED.")
        return 0
    print(f"\n❌ {results.count(False)} of {len(results)} evaluation suites FAILED.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
