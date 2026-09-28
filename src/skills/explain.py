"""Explainability Engine — Generates transparent 'Why Selected' and 'Why Rejected' traces.

Ensures every agent orchestration decision is inspectable, debuggable, and justified
against the user's explicit preferences, domain requirements, and detected conflicts.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SelectedSkillRationale:
    """Rationale for selecting a skill into the active stack."""
    skill_id: str
    slot: str
    confidence: float             # 0.0 to 1.0
    rationale: str                # e.g., 'Matches explicit user technology request (Stripe)'
    matched_signals: List[str]    # e.g., ['explicit_mention', 'capability_match', 'quality_boost']
    estimated_token_cost: int = 1500


@dataclass
class RejectedSkillRationale:
    """Rationale for rejecting a candidate skill from the active stack."""
    skill_id: str
    slot: str
    reason: str                   # e.g., 'User specified Stripe; rejected competing PayPal'
    rejection_type: str           # 'negative_constraint' | 'conflict' | 'suboptimal_score' | 'redundant'
    competing_selected: Optional[str] = None


@dataclass
class ExplainabilityReport:
    """Comprehensive decision report explaining skill composition."""
    query: str
    stack_id: str
    selected: List[SelectedSkillRationale] = field(default_factory=list)
    rejected: List[RejectedSkillRationale] = field(default_factory=list)
    conflicts_resolved: List[Dict[str, Any]] = field(default_factory=list)
    optimization_summary: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query": self.query,
            "stack_id": self.stack_id,
            "selected": [asdict(s) for s in self.selected],
            "rejected": [asdict(r) for r in self.rejected],
            "conflicts_resolved": self.conflicts_resolved,
            "optimization_summary": self.optimization_summary,
        }

    def format_cli(self) -> str:
        """Format a beautiful terminal view of the explainability trace."""
        lines = []
        lines.append(f"USER REQUEST: \"{self.query}\"")
        lines.append(f"STACK ID:     {self.stack_id}")
        lines.append("")
        lines.append("SELECTED SKILLS:")
        for s in self.selected:
            lines.append(f"  ✓ {s.skill_id:<24} → {s.rationale} ({s.slot}, {s.confidence:.0%})")
        lines.append("")
        if self.rejected:
            lines.append("REJECTED CANDIDATES:")
            for r in self.rejected:
                comp = f" (selected {r.competing_selected} instead)" if r.competing_selected else ""
                lines.append(f"  ✗ {r.skill_id:<24} → {r.reason}{comp}")
            lines.append("")
        if self.conflicts_resolved:
            lines.append("CONFLICTS RESOLVED:")
            for c in self.conflicts_resolved:
                lines.append(f"  ⚡ {c.get('description', 'Conflict')} → Resolved by: {c.get('resolution_rule', 'Priority rule')}")
            lines.append("")
        if self.optimization_summary:
            lines.append("OPTIMIZATION SUMMARY:")
            for k, v in self.optimization_summary.items():
                lines.append(f"  • {k:<20}: {v}")
        return "\n".join(lines)


class ExplainabilityTracer:
    """Builder for explainability reports during skill composition."""

    def __init__(self, query: str, stack_id: str = "") -> None:
        self.query = query
        self.stack_id = stack_id or f"stack_{abs(hash(query)) % 10000:04d}"
        self.report = ExplainabilityReport(query=query, stack_id=self.stack_id)

    def record_selection(
        self,
        skill_id: str,
        slot: str,
        confidence: float,
        rationale: str,
        matched_signals: Optional[List[str]] = None,
        estimated_token_cost: int = 1500,
    ) -> None:
        self.report.selected.append(
            SelectedSkillRationale(
                skill_id=skill_id,
                slot=slot,
                confidence=confidence,
                rationale=rationale,
                matched_signals=matched_signals or [],
                estimated_token_cost=estimated_token_cost,
            )
        )

    def record_rejection(
        self,
        skill_id: str,
        slot: str,
        reason: str,
        rejection_type: str,
        competing_selected: Optional[str] = None,
    ) -> None:
        self.report.rejected.append(
            RejectedSkillRationale(
                skill_id=skill_id,
                slot=slot,
                reason=reason,
                rejection_type=rejection_type,
                competing_selected=competing_selected,
            )
        )

    def record_conflict(self, description: str, resolution_rule: str, winner: str, loser: str) -> None:
        self.report.conflicts_resolved.append({
            "description": description,
            "resolution_rule": resolution_rule,
            "winner": winner,
            "loser": loser,
        })

    def set_optimization_summary(self, summary: Dict[str, Any]) -> None:
        self.report.optimization_summary = summary

    def build(self) -> ExplainabilityReport:
        return self.report
