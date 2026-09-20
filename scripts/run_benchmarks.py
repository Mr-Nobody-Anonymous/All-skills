#!/usr/bin/env python3
"""Routing benchmark evaluation harness.

Measures routing accuracy (exact match, top-3 recall, false positives, out-of-domain rejection)
and execution latency percentiles (p50, p95, p99).

Usage:
    python scripts/run_benchmarks.py
    python scripts/run_benchmarks.py --perf
    python scripts/run_benchmarks.py --json
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
from pathlib import Path
from typing import Any, Dict, List

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from skills.registry import Registry, SkillEntry, load_registry
from skills.router import Router


def load_unified_registry(repo_root: Path) -> Registry:
    """Load canonical skills and active harness skills into a single index."""
    reg = load_registry(repo_root)
    existing_ids = {e.id for e in reg.entries}

    # Add active harness skills
    agents_dir = repo_root / ".agents" / "skills"
    if agents_dir.exists():
        for sdir in sorted(agents_dir.iterdir()):
            if sdir.is_dir() and not sdir.name.startswith("."):
                sid = sdir.name
                if sid in existing_ids:
                    continue
                skill_md = sdir / "SKILL.md"
                if not skill_md.exists():
                    continue
                try:
                    from skills.frontmatter import parse_frontmatter
                    meta, _ = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
                except Exception:
                    continue

                entry = SkillEntry(
                    id=sid,
                    name=meta.get("name", sid),
                    category=meta.get("category", "active-harness"),
                    description=meta.get("description", ""),
                    path=f".agents/skills/{sid}",
                    aliases=meta.get("aliases", []) or [],
                    triggers=meta.get("triggers", []) or [],
                    keywords=meta.get("keywords", []) or [],
                    dependencies=meta.get("dependencies", []) or [],
                    composes_with=meta.get("composes_with", []) or [],
                    suggests_after=meta.get("suggests_after", []) or [],
                    source=meta.get("source"),
                    enabled=True,
                    risk=meta.get("risk", "low"),
                    version=meta.get("version", "1.0.0"),
                    lifecycle="enabled",
                    capabilities=meta.get("capabilities", []) or []
                )
                reg.entries.append(entry)
                existing_ids.add(sid)
    return reg


def run_benchmark(cases_file: Path, threshold: float = 22.0, measure_perf: bool = True) -> dict:
    if not cases_file.exists():
        raise FileNotFoundError(f"Benchmark cases not found at {cases_file}")

    with open(cases_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    cases = data.get("cases", [])
    reg = load_unified_registry(REPO_ROOT)
    router = Router(reg)

    positive_cases = [c for c in cases if c.get("type") == "positive"]
    negative_cases = [c for c in cases if c.get("type") == "negative"]

    exact_matches = 0
    top3_recalls = 0
    unknown_rejections = 0
    false_positives = 0

    eval_details: List[dict] = []

    # 1. Evaluate positive cases
    for case in positive_cases:
        prompt = case["prompt"]
        expected = set(case["expected"])
        matches = router.route(prompt, top_k=3)

        top_match = matches[0].skill.id if matches and matches[0].score >= threshold else None
        top3_ids = [m.skill.id for m in matches if m.score >= threshold]

        is_exact = (top_match in expected) if top_match else False
        is_top3 = any(tid in expected for tid in top3_ids)

        if is_exact:
            exact_matches += 1
        if is_top3:
            top3_recalls += 1

        eval_details.append({
            "case_id": case["id"],
            "type": "positive",
            "prompt": prompt,
            "expected": list(expected),
            "matched": top_match,
            "top3": top3_ids,
            "exact": is_exact,
            "recall": is_top3,
            "score": matches[0].score if matches else 0.0
        })

    # 2. Evaluate negative (out-of-domain) cases
    for case in negative_cases:
        prompt = case["prompt"]
        matches = router.route(prompt, top_k=1)
        top_score = matches[0].score if matches else 0.0

        # Out-of-domain is rejected if no match OR top score is below threshold
        rejected = (not matches) or (top_score < threshold)
        if rejected:
            unknown_rejections += 1
        else:
            false_positives += 1

        eval_details.append({
            "case_id": case["id"],
            "type": "negative",
            "prompt": prompt,
            "rejected": rejected,
            "top_candidate": matches[0].skill.id if matches else None,
            "score": top_score
        })

    pos_total = len(positive_cases) or 1
    neg_total = len(negative_cases) or 1

    exact_pct = round((exact_matches / pos_total) * 100, 1)
    recall_pct = round((top3_recalls / pos_total) * 100, 1)
    unknown_pct = round((unknown_rejections / neg_total) * 100, 1)
    fp_pct = round((false_positives / neg_total) * 100, 1)

    # 3. Latency measurement
    latencies_ms: List[float] = []
    if measure_perf:
        # Warmup
        for _ in range(5):
            router.route("test prompt", top_k=3)

        test_prompts = [c["prompt"] for c in cases]
        for _ in range(20):
            for p in test_prompts:
                t0 = time.perf_counter()
                router.route(p, top_k=3)
                t1 = time.perf_counter()
                latencies_ms.append((t1 - t0) * 1000.0)

    p50 = round(statistics.median(latencies_ms), 3) if latencies_ms else 0.0
    p95 = round(statistics.quantiles(latencies_ms, n=20)[18], 3) if len(latencies_ms) >= 20 else p50
    p99 = round(statistics.quantiles(latencies_ms, n=100)[98], 3) if len(latencies_ms) >= 100 else p95

    return {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "threshold": threshold,
        "cases_total": len(cases),
        "positive_cases": len(positive_cases),
        "negative_cases": len(negative_cases),
        "exact_match_pct": exact_pct,
        "top3_recall_pct": recall_pct,
        "unknown_detection_pct": unknown_pct,
        "false_positives_pct": fp_pct,
        "latencies_ms": {
            "p50": p50,
            "p95": p95,
            "p99": p99,
            "samples": len(latencies_ms)
        },
        "details": eval_details
    }


def print_report(results: dict) -> None:
    print("\n" + "=" * 48)
    print("           ROUTING INTENT BENCHMARK")
    print("=" * 48)
    print(f"Exact match:       {results['exact_match_pct']:>6}%")
    print(f"Top-3 recall:      {results['top3_recall_pct']:>6}%")
    print(f"Unknown detection: {results['unknown_detection_pct']:>6}%")
    print(f"False positives:   {results['false_positives_pct']:>6}%")
    print("-" * 48)

    lat = results.get("latencies_ms", {})
    if lat:
        print("          LATENCY PERCENTILES (WARM CACHE)")
        print("-" * 48)
        print(f"p50 (median):      {lat['p50']:>6.3f} ms")
        print(f"p95:               {lat['p95']:>6.3f} ms")
        print(f"p99:               {lat['p99']:>6.3f} ms")
        print(f"Samples measured:  {lat['samples']:>6}")
    print("=" * 48 + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description="Routing Benchmark Harness")
    parser.add_argument("--cases", default=str(REPO_ROOT / "benchmarks" / "routing_cases.json"))
    parser.add_argument("--threshold", type=float, default=22.0, help="Score threshold for matching")
    parser.add_argument("--no-perf", action="store_true", help="Skip latency percentile measurements")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    results = run_benchmark(
        Path(args.cases),
        threshold=args.threshold,
        measure_perf=not args.no_perf
    )

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print_report(results)
    return 0


if __name__ == "__main__":
    sys.exit(main())
