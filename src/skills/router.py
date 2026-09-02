"""Skill router — maps natural language to skill IDs using layered scoring.

Each layer accumulates score rather than short-circuiting, so a request can be
matched on several signals at once:

1. Exact skill ID match            (100)
2. Alias exact match               (90)
3. Exact category match            (80)
4. Trigger phrase substring        (+ up to 100)
5. Keyword overlap                 (+ up to 40)
6. Capability/input/output match   (+ up to 15)
7. Token overlap                   (+ up to 25)
8. Dependency availability         (penalty when required tools are missing)
9. Quality-score boost             (up to +4, prefers maintained skills)

``RouteMatch`` is the public result of ``route()``; ``explain()`` returns
``RouteBreakdown`` objects that expose the per-signal breakdown so failures are
debuggable.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

from .dependencies import check_dependency
from .registry import Registry, SkillEntry


_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "for", "with", "by", "from", "as", "at",
    "this", "that", "these", "those", "i", "you", "me", "my", "we", "our",
    "it", "its", "they", "them", "their", "and", "or", "but", "if",
    "do", "does", "did", "doing", "have", "has", "had", "can", "could",
    "would", "should", "will", "shall", "may", "might", "must",
    "please", "help", "need", "want", "like", "get", "make",
    "go", "going", "some", "any", "all", "every", "no", "not",
    "into", "out", "up", "down", "over", "under", "again", "then",
    "than", "so", "very", "just", "about",
}


@dataclass
class RouteMatch:
    skill: SkillEntry
    score: float
    matched_on: str  # "id" | "alias" | "category" | "trigger" | "keyword" | "capability" | "token" | "composition"


@dataclass
class RouteBreakdown:
    skill: SkillEntry
    score: float
    primary_signal: str
    signals: Dict[str, float] = field(default_factory=dict)


class Router:
    def __init__(self, registry: Registry) -> None:
        self.registry = registry

    def route(self, query: str, top_k: int = 3) -> List[RouteMatch]:
        breakdowns = self.explain(query, top_k=top_k)
        return [
            RouteMatch(bd.skill, bd.score, bd.primary_signal)
            for bd in breakdowns
        ]

    def route_one(self, query: str) -> Optional[RouteMatch]:
        matches = self.route(query, top_k=1)
        return matches[0] if matches else None

    def explain(self, query: str, top_k: int = 3) -> List[RouteBreakdown]:
        """Score every enabled skill for ``query`` and return ordered breakdowns."""
        q = (query or "").strip().lower()
        if not q:
            return []
        # A bare category name activates every enabled skill in that category.
        category_hits = [
            e for e in self.registry.entries
            if e.enabled and q == e.category.lower()
        ]
        if category_hits:
            out = [
                RouteBreakdown(e, 80.0, "category", {"category": 80.0})
                for e in category_hits
            ]
            out.sort(key=lambda bd: bd.skill.id)
            return out[:top_k]
        breakdowns: List[RouteBreakdown] = []
        for entry in self.registry.entries:
            if not entry.enabled:
                continue
            result = self._score_one(q, entry)
            if result is None:
                continue
            score, primary, signals = result
            breakdowns.append(RouteBreakdown(entry, score, primary, signals))
        breakdowns.sort(key=lambda bd: (-bd.score, bd.skill.id))
        return breakdowns[:top_k]

    def route_chain(self, query: str, top_k: int = 5) -> List[RouteMatch]:
        """Return matching skills plus compatible follow-on skills in stable order."""
        matches = self.route(query, top_k=top_k)
        if not matches:
            return []
        ordered = list(matches)
        by_id = {match.skill.id: match for match in matches}
        for match in list(matches):
            for skill_id in match.skill.suggests_after + match.skill.composes_with:
                composed_score = max(match.score - 30.0, 1.0)
                if skill_id in by_id:
                    existing = by_id[skill_id]
                    if composed_score > existing.score:
                        existing.score = composed_score
                        existing.matched_on = "composition"
                    continue
                entry = self.registry.get(skill_id)
                if entry and entry.enabled:
                    composed = RouteMatch(entry, composed_score, "composition")
                    ordered.append(composed)
                    by_id[skill_id] = composed
        ordered.sort(key=lambda item: item.score, reverse=True)
        return ordered[:top_k]

    # ---- internals -------------------------------------------------------

    def _score_one(self, q: str, entry: SkillEntry) -> Optional[Tuple[float, str, Dict[str, float]]]:
        """Return (score, primary_signal, signals) for a single skill, or None."""
        signals: Dict[str, float] = {}
        # 1. Exact ID match
        if q == entry.id.lower():
            return 100.0, "id", {"id": 100.0}
        # 2. Alias exact
        for a in entry.aliases:
            if a and q == a.lower():
                return 90.0, "alias", {"alias": 90.0}
        # 3. Exact category match (the whole-category path is handled in explain()).
        if q == entry.category.lower():
            return 80.0, "category", {"category": 80.0}

        score = 0.0

        # 4. Trigger phrase substring (longer triggers score higher)
        best_trigger = 0.0
        for t in entry.triggers:
            tl = (t or "").lower().strip()
            if tl and tl in q:
                s = 70.0 + min(len(tl), 30)
                if s > best_trigger:
                    best_trigger = s
        if best_trigger:
            signals["trigger"] = round(best_trigger, 1)
            score += best_trigger

        # 5. Keyword overlap (fraction of the skill's keywords found in query)
        keyword_hits = 0
        total_keywords = 0
        for kw in entry.keywords:
            kwl = (kw or "").lower().strip()
            total_keywords += 1
            if kwl and (kwl in q or kwl.replace("-", " ") in q):
                keyword_hits += 1
        keyword_score = 0.0
        if total_keywords > 0 and keyword_hits > 0:
            keyword_score = (keyword_hits / total_keywords) * 40.0
            signals["keyword"] = round(keyword_score, 1)
            score += keyword_score

        # 6. Capability/input/output vocabulary match (semantic relevance)
        vocab = (
            [c for c in entry.capabilities]
            + [i for i in entry.inputs]
            + [o for o in entry.outputs]
        )
        cap_hits = sum(1 for term in vocab if term and term.lower() in q)
        if cap_hits:
            cap_score = min(cap_hits, 3) * 5.0
            signals["capability"] = round(cap_score, 1)
            score += cap_score

        # 7. Token overlap (fallback)
        q_tokens = [t for t in _WORD_RE.findall(q) if t not in _STOPWORDS]
        if q_tokens:
            hay_tokens: set[str] = set()
            hay_tokens.update(_WORD_RE.findall(entry.name.lower()))
            hay_tokens.update(_WORD_RE.findall(entry.description.lower()))
            for s in entry.aliases + entry.triggers + entry.keywords + entry.capabilities + entry.outputs:
                hay_tokens.update(_WORD_RE.findall(s.lower()))
            hay_tokens -= _STOPWORDS
            overlap = sum(1 for t in q_tokens if t in hay_tokens)
            if overlap > 0:
                token_score = (overlap / len(q_tokens)) * 25.0
                signals["token"] = round(token_score, 1)
                score += token_score

        # 8. Dependency availability penalty (only required, missing tools count)
        missing = self._missing_required(entry)
        if missing:
            penalty = -min(12.0, 3.0 * len(missing))
            signals["dependency_penalty"] = round(penalty, 1)
            score += penalty

        # 9. Quality-score boost (0-10 overall score -> up to +4)
        quality_score = entry.quality_score or 0.0
        if quality_score > 0:
            boost = (quality_score / 10.0) * 4.0
            signals["quality"] = round(boost, 2)
            score += boost

        if score <= 0:
            return None
        primary = (
            "trigger" if best_trigger
            else ("keyword" if keyword_hits > 0
                  else ("capability" if cap_hits > 0 else "token"))
        )
        return min(score, 100.0), primary, signals

    @staticmethod
    def _missing_required(entry: SkillEntry) -> List[str]:
        missing: List[str] = []
        for dep in entry.dependencies:
            status = check_dependency(entry.id, dep)
            if not status.available and status.optional is False:
                missing.append(dep)
        return missing