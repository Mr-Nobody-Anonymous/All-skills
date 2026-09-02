"""Skill router — maps natural language to skill IDs.

Strategy:
1. Exact skill ID match.
2. Alias match.
3. Keyword/trigger phrase matching (substring).
4. Token overlap scoring (fallback).
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

from .registry import Registry, SkillEntry


_WORD_RE = re.compile(r"[a-zA-Z][a-zA-Z0-9_-]+")
_STOPWORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "to", "of", "in", "on", "for", "with", "by", "from", "as", "at",
    "this", "that", "these", "those", "i", "you", "me", "my", "we", "our",
    "it", "its", "they", "them", "their", "and", "or", "but", "if",
    "do", "does", "did", "doing", "have", "has", "had", "can", "could",
    "would", "should", "will", "shall", "may", "might", "must",
    "please", "help", "need", "want", "like", "get", "make", "make",
    "go", "going", "some", "any", "all", "every", "no", "not",
    "into", "out", "up", "down", "over", "under", "again", "then",
    "than", "so", "very", "just", "about",
}


@dataclass
class RouteMatch:
    skill: SkillEntry
    score: float
    matched_on: str  # "id" | "alias" | "category" | "trigger" | "keyword" | "token"


class Router:
    def __init__(self, registry: Registry) -> None:
        self.registry = registry

    def route(self, query: str, top_k: int = 3) -> List[RouteMatch]:
        q = (query or "").strip().lower()
        if not q:
            return []
        category_matches = [
            RouteMatch(entry, 80.0, "category")
            for entry in self.registry.entries
            if entry.enabled and q == entry.category.lower()
        ]
        if category_matches:
            return sorted(category_matches, key=lambda item: item.skill.id)[:top_k]
        scored: List[RouteMatch] = []
        for entry in self.registry.entries:
            if not entry.enabled:
                continue
            m = self._score_one(q, entry)
            if m:
                scored.append(m)
        scored.sort(key=lambda x: x.score, reverse=True)
        return scored[:top_k]

    def route_one(self, query: str) -> Optional[RouteMatch]:
        matches = self.route(query, top_k=1)
        return matches[0] if matches else None

    def route_chain(self, query: str, top_k: int = 5) -> List[RouteMatch]:
        """Return matching skills plus compatible next skills in stable order."""
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

    def _score_one(self, q: str, entry: SkillEntry) -> Optional[RouteMatch]:
        # 1. Exact ID match
        if q == entry.id.lower():
            return RouteMatch(entry, 100.0, "id")
        # 2. Alias exact
        for a in entry.aliases:
            if q == a.lower():
                return RouteMatch(entry, 90.0, "alias")
        # 3. Exact category match supports category-level discovery.
        if q == entry.category.lower():
            return RouteMatch(entry, 80.0, "category")
        # 4. Trigger phrase substring (longer triggers score higher)
        best_trigger_score = 0.0
        matched_trigger = False
        for t in entry.triggers:
            tl = t.lower()
            if tl in q:
                score = 70.0 + min(len(tl), 30)
                if score > best_trigger_score:
                    best_trigger_score = score
                matched_trigger = True
        # 4. Keyword overlap
        keyword_hits = 0
        total_keywords = 0
        for kw in entry.keywords:
            kwl = kw.lower()
            total_keywords += 1
            if kwl in q or kwl.replace("-", " ") in q:
                keyword_hits += 1
        keyword_score = 0.0
        if total_keywords > 0 and keyword_hits > 0:
            keyword_score = (keyword_hits / total_keywords) * 40.0
        # 5. Token overlap (fallback)
        q_tokens = [t for t in _WORD_RE.findall(q) if t not in _STOPWORDS]
        if not q_tokens:
            return None
        # Build haystack tokens
        hay_tokens = set()
        hay_tokens.update(_WORD_RE.findall(entry.name.lower()))
        hay_tokens.update(_WORD_RE.findall(entry.description.lower()))
        for s in entry.aliases:
            hay_tokens.update(_WORD_RE.findall(s.lower()))
        for s in entry.triggers:
            hay_tokens.update(_WORD_RE.findall(s.lower()))
        for s in entry.keywords:
            hay_tokens.update(_WORD_RE.findall(s.lower()))
        hay_tokens -= _STOPWORDS
        overlap = sum(1 for t in q_tokens if t in hay_tokens)
        token_score = 0.0
        if overlap > 0:
            token_score = (overlap / len(q_tokens)) * 25.0
        # Combine
        score = best_trigger_score + keyword_score + token_score
        if score <= 0:
            return None
        if matched_trigger:
            return RouteMatch(entry, score, "trigger")
        if keyword_hits > 0:
            return RouteMatch(entry, score, "keyword")
        return RouteMatch(entry, score, "token")