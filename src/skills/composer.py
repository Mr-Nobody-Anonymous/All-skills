"""Intelligent Skill Stack Composer.

Solves the multi-slot capability coverage problem:
  Maximize: Capability Coverage - alpha * Token Cost - beta * Risk - Conflict Penalties
Constructs the minimal, conflict-free, high-reliability Skill Stack for any agent task
with complete explainability tracing.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .conflicts import ConflictResolver, load_conflicts
from .explain import ExplainabilityReport, ExplainabilityTracer
from .intent import AnalyzedIntent, IntentAnalyzer
from .registry import Registry, SkillEntry, load_registry
from .router import Router


@dataclass
class SkillStack:
    """A composed, minimal set of skills for executing an agent task."""
    stack_id: str
    query: str
    primary_domain: str
    skills: List[str]             # ordered list of selected skill IDs
    slot_mapping: Dict[str, str]  # slot -> skill_id
    total_token_cost: int
    quality_score: float          # composite 0-100 quality score
    explainability: ExplainabilityReport

    def to_dict(self) -> Dict[str, Any]:
        return {
            "stack_id": self.stack_id,
            "query": self.query,
            "primary_domain": self.primary_domain,
            "skills": self.skills,
            "slot_mapping": self.slot_mapping,
            "total_token_cost": self.total_token_cost,
            "quality_score": round(self.quality_score, 1),
            "explainability": self.explainability.to_dict(),
        }


# Canonical fallback skills for common capability slots
SLOT_CANONICAL_FALLBACKS: Dict[str, List[str]] = {
    "frontend": ["frontend-engineering", "react-state-management", "tailwind-design-system", "design-system"],
    "backend": ["api-and-interface-design", "api-designer", "grpc-protobuf-microservices"],
    "database": ["database-design", "postgresql-optimization-tuning", "drizzle-orm-expert", "prisma-expert"],
    "authentication": ["iam-zero-trust-identity", "marketplace-rbac-audit"],
    "payments": ["fintech-payment-gateways", "saas-mvp-launcher"],
    "security": ["security-sandboxing-guardrails", "top-web-vulnerabilities", "appsec-sast-dast-remediation", "threat-modeling-stride-pasta"],
    "testing": ["tdd", "playwright-skill", "browser-automation", "code-showcase-systematic-debugging"],
    "deployment": ["cloud-devops", "ci-cd-and-automation", "kubernetes-architect", "terraform-infrastructure"],
    "observability": ["metrics-alerting-prometheus-grafana", "distributed-tracing-opentelemetry", "site-reliability-engineering-sre"],
}


class SkillComposer:
    """Intelligent Skill Stack Composer with Explainability Tracing."""

    def __init__(
        self,
        registry: Optional[Registry] = None,
        workspace_root: Optional[Path] = None,
    ) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.registry = registry or load_registry(self.workspace_root)
        self.router = Router(self.registry)
        self.conflict_resolver = ConflictResolver(load_conflicts(self.workspace_root))
        self.intent_analyzer = IntentAnalyzer()

    def compose(
        self,
        query: str,
        project_config: Optional[Dict[str, Any]] = None,
        max_skills: int = 8,
        token_budget: int = 15000,
    ) -> SkillStack:
        """Compose the minimal, conflict-free, high-reliability skill stack for a query."""
        # 1. Analyze Intent
        intent: AnalyzedIntent = self.intent_analyzer.analyze(query)
        stack_id = f"stack_{abs(hash(query)) % 100000:05d}"
        tracer = ExplainabilityTracer(query=query, stack_id=stack_id)

        selected_skills: List[str] = []
        slot_mapping: Dict[str, str] = {}
        total_tokens = 0

        # Quality lookup table (from registry if available)
        quality_lookup: Dict[str, float] = {}
        for entry in self.registry.entries:
            # Assume 0-10 or 0-100; normalize to 0-100 scale
            raw_q = getattr(entry, "quality", None)
            if isinstance(raw_q, dict):
                score = float(raw_q.get("overall_score", 8.0)) * 10.0
            elif isinstance(raw_q, (int, float)):
                score = float(raw_q) * 10.0 if raw_q <= 10.0 else float(raw_q)
            else:
                score = 85.0
            quality_lookup[entry.id] = score

        # 2. Per-Slot Candidate Retrieval & Selection
        for req in intent.requirements:
            slot = req.slot
            slot_candidates = self._find_candidates_for_slot(req, intent)

            # Evaluate each candidate against negative preferences
            filtered_candidates = []
            for cand, cand_score, match_sig in slot_candidates:
                # Check negative constraints
                neg_hit = False
                all_negatives = set(req.negative_tech).union(intent.negative_preferences)
                for neg in all_negatives:
                    if neg in cand.lower():
                        tracer.record_rejection(
                            skill_id=cand,
                            slot=slot,
                            reason=f"Matched negative constraint / exclusion '{neg}'",
                            rejection_type="negative_constraint",
                        )
                        neg_hit = True
                        break
                if not neg_hit:
                    filtered_candidates.append((cand, cand_score, match_sig))

            if not filtered_candidates:
                continue

            # Pick top candidate for this slot
            best_cand, best_score, match_sig = filtered_candidates[0]

            # Record any alternatives that were rejected
            for alt_cand, alt_score, _ in filtered_candidates[1:4]:
                tracer.record_rejection(
                    skill_id=alt_cand,
                    slot=slot,
                    reason=f"Suboptimal ranking score ({alt_score:.1f} vs {best_score:.1f}) for slot '{slot}'",
                    rejection_type="suboptimal_score",
                    competing_selected=best_cand,
                )

            selected_skills.append(best_cand)
            slot_mapping[slot] = best_cand
            total_tokens += 1500

            tracer.record_selection(
                skill_id=best_cand,
                slot=slot,
                confidence=min(1.0, best_score / 100.0),
                rationale=f"Best capability match for slot '{slot}' (signals: {', '.join(match_sig)})",
                matched_signals=match_sig,
                estimated_token_cost=1500,
            )

        # 3. Conflict Resolution
        resolved_skills, resolutions = self.conflict_resolver.resolve(
            candidate_skills=selected_skills,
            user_preferences=intent.explicit_mentions,
            project_config=project_config,
            skill_quality_scores=quality_lookup,
        )

        for res in resolutions:
            tracer.record_conflict(
                description=res["description"],
                resolution_rule=res["resolution_rule"],
                winner=res["winner"],
                loser=res["loser"],
            )
            tracer.record_rejection(
                skill_id=res["loser"],
                slot=self._get_slot_for_skill(res["loser"], slot_mapping),
                reason=f"Conflict with {res['winner']} resolved by {res['resolution_rule']}",
                rejection_type="conflict",
                competing_selected=res["winner"],
            )

        # Rebuild clean slot mapping
        clean_mapping = {
            slot: skill for slot, skill in slot_mapping.items()
            if skill in resolved_skills
        }

        # 4. Token Budget Optimization
        if len(resolved_skills) > max_skills or total_tokens > token_budget:
            # Retain critical slots first
            critical_slots = {r.slot for r in intent.requirements if r.critical}
            pruned = [s for s in resolved_skills if any(clean_mapping.get(cs) == s for cs in critical_slots)]
            for s in resolved_skills:
                if s not in pruned and len(pruned) < max_skills:
                    pruned.append(s)
                elif s not in pruned:
                    tracer.record_rejection(
                        skill_id=s,
                        slot=self._get_slot_for_skill(s, clean_mapping),
                        reason="Pruned to stay within token & skill cardinality budget",
                        rejection_type="redundant",
                    )
            resolved_skills = pruned

        # 5. Composite Quality Score
        scores = [quality_lookup.get(s, 85.0) for s in resolved_skills]
        avg_quality = sum(scores) / len(scores) if scores else 85.0

        tracer.set_optimization_summary({
            "slots_analyzed": len(intent.slots_needed),
            "slots_covered": len(clean_mapping),
            "total_candidates_evaluated": len(selected_skills),
            "final_skill_count": len(resolved_skills),
            "estimated_tokens": len(resolved_skills) * 1500,
            "average_quality": round(avg_quality, 1),
            "conflicts_resolved_count": len(resolutions),
        })

        return SkillStack(
            stack_id=stack_id,
            query=query,
            primary_domain=intent.primary_domain,
            skills=resolved_skills,
            slot_mapping=clean_mapping,
            total_token_cost=len(resolved_skills) * 1500,
            quality_score=avg_quality,
            explainability=tracer.build(),
        )

    def _find_candidates_for_slot(
        self,
        req: Any,
        intent: AnalyzedIntent,
    ) -> List[Tuple[str, float, List[str]]]:
        """Find and rank candidate skills for a specific capability requirement."""
        slot = req.slot
        candidates: List[Tuple[str, float, List[str]]] = []
        seen = set()

        # 1. Direct preferred technology matches
        for pref in req.preferred_tech:
            # Query router with preferred technology keyword
            matches = self.router.route(f"{pref} {slot}", top_k=3)
            for m in matches:
                if m.skill.id not in seen:
                    signals = ["explicit_technology_mention"]
                    if m.matched_on:
                        signals.append(f"router_{m.matched_on}")
                    score = m.score + 25.0  # boost for explicit tech mention
                    candidates.append((m.skill.id, score, signals))
                    seen.add(m.skill.id)

        # 2. Domain & slot keyword matches
        slot_query = f"{slot} {req.description}"
        matches = self.router.route(slot_query, top_k=5)
        for m in matches:
            if m.skill.id not in seen:
                signals = ["slot_semantic_match"]
                if m.matched_on:
                    signals.append(f"router_{m.matched_on}")
                candidates.append((m.skill.id, m.score, signals))
                seen.add(m.skill.id)

        # 3. Predefined canonical fallbacks
        if not candidates and slot in SLOT_CANONICAL_FALLBACKS:
            for fallback in SLOT_CANONICAL_FALLBACKS[slot]:
                if self.registry.get(fallback) is not None and fallback not in seen:
                    candidates.append((fallback, 60.0, ["canonical_slot_fallback"]))
                    seen.add(fallback)

        # Sort by score descending
        candidates.sort(key=lambda x: x[1], reverse=True)
        return candidates

    def _get_slot_for_skill(self, skill_id: str, mapping: Dict[str, str]) -> str:
        for slot, s in mapping.items():
            if s == skill_id:
                return slot
        return "general"
