"""SR-Agents / SRA-Bench Style Retrieval Benchmark for All-Skills Router.

Evaluates natural language skill routing across multi-domain queries, computing:
- Precision@K (P@1, P@3, P@5)
- Recall@K (R@5)
- Mean Reciprocal Rank (MRR)
- Average routing latency (ms)
"""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

BENCHMARK_CASES: List[Dict[str, Any]] = [
    {
        "query": "build android jetpack compose reactive state",
        "expected_skill": "android-compose",
        "domain": "mobile"
    },
    {
        "query": "apache kafka event streaming consumer group partition",
        "expected_skill": "apache-kafka",
        "domain": "data"
    },
    {
        "query": "bioinformatics genomic sequence alignment blast fasta",
        "expected_skill": "bioinformatics",
        "domain": "scientific"
    },
    {
        "query": "gdpr compliance data protection impact assessment dpia",
        "expected_skill": "gdpr",
        "domain": "legal"
    },
    {
        "query": "esp32 freertos wifi ble firmware development",
        "expected_skill": "esp32",
        "domain": "embedded"
    },
    {
        "query": "unreal engine 5 c++ gameplay nanite lumen",
        "expected_skill": "unreal-engine",
        "domain": "game"
    },
    {
        "query": "tauri lightweight desktop app rust webview",
        "expected_skill": "tauri",
        "domain": "desktop"
    },
    {
        "query": "linux kernel loadable module character device driver",
        "expected_skill": "linux-kernel",
        "domain": "os"
    },
    {
        "query": "wireshark deep packet inspection tls handshake",
        "expected_skill": "wireshark",
        "domain": "networking"
    },
    {
        "query": "kubernetes pod cost allocation opencost kubecost",
        "expected_skill": "kubernetes-cost",
        "domain": "finops"
    },
    {
        "query": "retrieval augmented generation document chunking vector embeddings",
        "expected_skill": "rag",
        "domain": "ai"
    },
    {
        "query": "prometheus metrics promql query alertmanager rules",
        "expected_skill": "prometheus",
        "domain": "observability"
    }
]


@dataclass
class BenchmarkResult:
    total_queries: int
    precision_at_1: float
    precision_at_3: float
    precision_at_5: float
    mrr: float
    avg_latency_ms: float
    details: List[Dict[str, Any]]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class RetrievalBenchmark:
    """Retrieval benchmark engine."""

    def __init__(self, repo_root: Optional[Path] = None):
        self.repo_root = repo_root or REPO_ROOT
        from src.skills.registry import Registry
        from src.skills.router import Router
        self.registry = Registry.load(self.repo_root / "manifest.json", self.repo_root / "skills")
        self.router = Router(self.registry)

    def run_benchmark(self) -> BenchmarkResult:
        hits_at_1 = 0
        hits_at_3 = 0
        hits_at_5 = 0
        reciprocal_ranks = []
        latencies = []
        details = []

        for case in BENCHMARK_CASES:
            query = case["query"]
            expected = case["expected_skill"]

            start = time.perf_counter()
            matches = self.router.route(query, top_k=5)
            elapsed_ms = (time.perf_counter() - start) * 1000.0
            latencies.append(elapsed_ms)

            matched_ids = [m.skill.id.split(".")[-1] for m in matches]

            rank = -1
            for idx, mid in enumerate(matched_ids):
                if mid == expected or expected in mid:
                    rank = idx + 1
                    break

            if rank == 1:
                hits_at_1 += 1
            if 1 <= rank <= 3:
                hits_at_3 += 1
            if 1 <= rank <= 5:
                hits_at_5 += 1

            rr = 1.0 / rank if rank > 0 else 0.0
            reciprocal_ranks.append(rr)

            details.append({
                "query": query,
                "expected": expected,
                "matched": matched_ids,
                "rank": rank,
                "latency_ms": round(elapsed_ms, 2)
            })

        n = len(BENCHMARK_CASES)
        return BenchmarkResult(
            total_queries=n,
            precision_at_1=round(hits_at_1 / n, 4),
            precision_at_3=round(hits_at_3 / n, 4),
            precision_at_5=round(hits_at_5 / n, 4),
            mrr=round(sum(reciprocal_ranks) / n, 4),
            avg_latency_ms=round(sum(latencies) / n, 2),
            details=details
        )


def main() -> int:
    print("[*] Initializing All-Skills SRA Retrieval Benchmark...")
    benchmark = RetrievalBenchmark()
    res = benchmark.run_benchmark()

    print("\n=== Retrieval Benchmark Results ===")
    print(f"Total Queries Evaluated : {res.total_queries}")
    print(f"Precision @ 1           : {res.precision_at_1 * 100:.1f}%")
    print(f"Precision @ 3           : {res.precision_at_3 * 100:.1f}%")
    print(f"Precision @ 5           : {res.precision_at_5 * 100:.1f}%")
    print(f"Mean Reciprocal Rank    : {res.mrr:.4f}")
    print(f"Avg Latency per Route   : {res.avg_latency_ms:.2f} ms")
    print("===================================\n")

    out_file = REPO_ROOT / "benchmarks" / "retrieval_benchmark_results.json"
    out_file.write_text(json.dumps(res.to_dict(), indent=2), encoding="utf-8")
    print(f"[+] Detailed telemetry saved to {out_file.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    main()
