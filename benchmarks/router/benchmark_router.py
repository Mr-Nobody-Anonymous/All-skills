#!/usr/bin/env python3
"""
benchmark_router.py — Empirical benchmark evaluation harness for the Agent Skills router.
Evaluates:
- Recall@1, Recall@3, Recall@5
- False-Activation Rate
- Out-of-Domain Rejection Rate
- Routing Latency (mean, P95, P99)
- Ambiguous intent and category confusion
"""

import json
import time
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from skills.registry import Registry
from skills.router import Router

def run_benchmark():
    cases_file = ROOT / "benchmarks" / "routing_cases.json"
    if not cases_file.exists():
        print(f"Error: {cases_file} not found")
        sys.exit(1)

    with open(cases_file, "r", encoding="utf-8") as f:
        bench_data = json.load(f)

    cases = bench_data.get("cases", [])
    print(f"Loaded {len(cases)} benchmark cases from {cases_file}")

    # Load canonical registry & router
    from skills.registry import load_registry
    registry = load_registry(ROOT)
    router = Router(registry)

    positive_cases = [c for c in cases if c.get("type", "positive") == "positive"]
    negative_cases = [c for c in cases if c.get("type") in ("negative", "ood", "out-of-domain")]

    hits_at_1 = 0
    hits_at_3 = 0
    hits_at_5 = 0
    latencies = []

    case_details = []

    for c in positive_cases:
        prompt = c["prompt"]
        expected = set(c.get("expected", []))
        
        t0 = time.perf_counter()
        results = router.route(prompt, top_k=5)
        dt = (time.perf_counter() - t0) * 1000.0  # ms
        latencies.append(dt)

        top_ids = [r.skill.id for r in results]
        
        hit_1 = bool(top_ids and top_ids[0] in expected)
        hit_3 = any(tid in expected for tid in top_ids[:3])
        hit_5 = any(tid in expected for tid in top_ids[:5])

        if hit_1:
            hits_at_1 += 1
        if hit_3:
            hits_at_3 += 1
        if hit_5:
            hits_at_5 += 1

        case_details.append({
            "id": c.get("id"),
            "prompt": prompt,
            "type": "positive",
            "expected": list(expected),
            "routed": top_ids,
            "scores": [round(r.score, 2) for r in results],
            "hit@1": hit_1,
            "hit@3": hit_3,
            "latency_ms": round(dt, 3)
        })

    # Test out-of-domain / negative cases
    rejections = 0
    for c in negative_cases:
        prompt = c["prompt"]
        t0 = time.perf_counter()
        results = router.route(prompt, top_k=1)
        dt = (time.perf_counter() - t0) * 1000.0
        latencies.append(dt)

        is_rejected = len(results) == 0 or (results and results[0].score < 40.0)
        if is_rejected:
            rejections += 1

        case_details.append({
            "id": c.get("id"),
            "prompt": prompt,
            "type": "negative",
            "is_rejected": is_rejected,
            "routed": [r.skill.id for r in results],
            "latency_ms": round(dt, 3)
        })

    n_pos = len(positive_cases) or 1
    n_neg = len(negative_cases) or 1

    r_at_1 = (hits_at_1 / n_pos) * 100.0
    r_at_3 = (hits_at_3 / n_pos) * 100.0
    r_at_5 = (hits_at_5 / n_pos) * 100.0
    ood_rejection_rate = (rejections / n_neg) * 100.0
    false_activation_rate = 100.0 - ood_rejection_rate

    latencies.sort()
    mean_lat = sum(latencies) / len(latencies) if latencies else 0.0
    p95_lat = latencies[int(len(latencies) * 0.95)] if latencies else 0.0
    p99_lat = latencies[int(len(latencies) * 0.99)] if latencies else 0.0

    summary = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_cases": len(cases),
        "positive_cases": len(positive_cases),
        "negative_cases": len(negative_cases),
        "recall_at_1_pct": round(r_at_1, 2),
        "recall_at_3_pct": round(r_at_3, 2),
        "recall_at_5_pct": round(r_at_5, 2),
        "ood_rejection_rate_pct": round(ood_rejection_rate, 2),
        "false_activation_rate_pct": round(false_activation_rate, 2),
        "latency_ms": {
            "mean": round(mean_lat, 3),
            "p95": round(p95_lat, 3),
            "p99": round(p99_lat, 3)
        },
        "status": "PASS" if r_at_3 >= 85.0 else "WARN"
    }

    out_file = ROOT / "benchmarks" / "router" / "benchmark_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump({"summary": summary, "cases": case_details}, f, indent=2)

    print("\n" + "=" * 65)
    print("9-SIGNAL ROUTER BENCHMARK RESULTS")
    print("=" * 65)
    print(f"Total Test Cases:           {len(cases)}")
    print(f"Recall@1:                   {r_at_1:.1f}%")
    print(f"Recall@3:                   {r_at_3:.1f}%")
    print(f"Recall@5:                   {r_at_5:.1f}%")
    print(f"Out-of-Domain Rejection:    {ood_rejection_rate:.1f}%")
    print(f"False Activation Rate:      {false_activation_rate:.1f}%")
    print(f"Mean Latency:               {mean_lat:.3f} ms")
    print(f"P95 Latency:                {p95_lat:.3f} ms")
    print(f"Status:                     {summary['status']}")
    print(f"Detailed Report:            {out_file}")
    print("=" * 65 + "\n")

    return summary

if __name__ == "__main__":
    run_benchmark()
