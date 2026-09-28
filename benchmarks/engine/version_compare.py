"""Skill Version Comparison & Regression Analysis Engine.

Tracks performance trends across releases (v1.2.0 -> v1.3.0 -> v1.4.0) and automatically
detects regressions in correctness, latency, token consumption, and tool calling.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from .evaluator import BenchmarkResult


@dataclass
class VersionDiff:
    """Detailed diff between two consecutive skill versions."""
    base_version: str
    target_version: str
    correctness_delta: float      # e.g., +4.4 or -3.7
    token_delta: int              # e.g., -120 or +450
    latency_delta_ms: float
    tool_calls_delta: float
    composite_delta: float
    is_regression: bool
    regression_reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class VersionComparisonReport:
    """Historical version comparison for a skill."""
    skill_id: str
    versions_tested: List[str]
    history: List[BenchmarkResult]
    diffs: List[VersionDiff]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "versions_tested": self.versions_tested,
            "history": [h.to_dict() for h in self.history],
            "diffs": [d.to_dict() for d in self.diffs],
        }

    def format_cli(self) -> str:
        lines = [
            f"Version Comparison: {self.skill_id}",
            "─" * 40,
        ]
        for h in self.history:
            lines.append(f"v{h.version:<7} → {h.composite_score:.1f}% composite | {h.avg_token_cost} tokens | {h.avg_latency_ms:.1f}ms")

        lines.append("")
        lines.append("Version Transitions:")
        for d in self.diffs:
            arrow = "↓ REGRESSION" if d.is_regression else "↑ IMPROVEMENT"
            sym = "⚠️" if d.is_regression else "✅"
            lines.append(f"  {sym} v{d.base_version} → v{d.target_version}: {arrow} ({d.composite_delta:+.1f}%)")
            for r in d.regression_reasons:
                lines.append(f"      • {r}")
        return "\n".join(lines)


class VersionComparator:
    """Compares benchmark evaluations across skill revisions."""

    @staticmethod
    def compare_two(v1: BenchmarkResult, v2: BenchmarkResult) -> VersionDiff:
        """Compute diff between two benchmark evaluation runs."""
        c_delta = round(v2.correctness_pct - v1.correctness_pct, 1)
        t_delta = v2.avg_token_cost - v1.avg_token_cost
        l_delta = round(v2.avg_latency_ms - v1.avg_latency_ms, 1)
        tc_delta = round(v2.avg_tool_calls - v1.avg_tool_calls, 1)
        comp_delta = round(v2.composite_score - v1.composite_score, 1)

        reasons = []
        is_regression = False

        # Thresholds for regression
        if comp_delta < -2.0:
            is_regression = True
            reasons.append(f"Composite score dropped by {abs(comp_delta):.1f}%")
        if c_delta < -3.0:
            is_regression = True
            reasons.append(f"Correctness dropped from {v1.correctness_pct:.1f}% to {v2.correctness_pct:.1f}%")
        if t_delta > 500:
            is_regression = True
            reasons.append(f"Token cost spiked by +{t_delta} tokens ({t_delta / max(1, v1.avg_token_cost):.1%})")
        if v2.security_violations > v1.security_violations:
            is_regression = True
            reasons.append(f"Security violations increased (+{v2.security_violations - v1.security_violations})")

        return VersionDiff(
            base_version=v1.version,
            target_version=v2.version,
            correctness_delta=c_delta,
            token_delta=t_delta,
            latency_delta_ms=l_delta,
            tool_calls_delta=tc_delta,
            composite_delta=comp_delta,
            is_regression=is_regression,
            regression_reasons=reasons,
        )

    @classmethod
    def analyze_history(cls, skill_id: str, results: List[BenchmarkResult]) -> VersionComparisonReport:
        """Analyze a progression of multiple version evaluations."""
        diffs = []
        for i in range(len(results) - 1):
            diffs.append(cls.compare_two(results[i], results[i + 1]))

        return VersionComparisonReport(
            skill_id=skill_id,
            versions_tested=[r.version for r in results],
            history=results,
            diffs=diffs,
        )
