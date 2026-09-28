"""Intent Analyzer & Request Decomposer.

Extracts semantic requirements, capability slots (frontend, backend, database, auth,
payments, security, testing, deployment, etc.), explicit constraints, and technology
preferences from natural language requests.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Set


@dataclass
class IntentRequirement:
    """A decomposed requirement from user intent."""
    slot: str                     # e.g., 'frontend', 'database', 'auth', 'payments', 'security', 'testing'
    description: str              # e.g., 'relational persistent storage'
    preferred_tech: List[str] = field(default_factory=list) # e.g., ['postgres', 'postgresql']
    negative_tech: List[str] = field(default_factory=list)  # e.g., ['mongodb']
    critical: bool = True         # whether requirement is mandatory for task success


@dataclass
class AnalyzedIntent:
    """Complete analyzed intent representation."""
    raw_query: str
    primary_domain: str
    action_type: str              # 'build', 'debug', 'audit', 'optimize', 'migrate', 'test', 'explain'
    slots_needed: List[str]       # list of required slots
    requirements: List[IntentRequirement]
    explicit_mentions: Set[str]   # raw detected keywords like 'stripe', 'react'
    constraints: Dict[str, Any] = field(default_factory=dict)
    negative_preferences: Set[str] = field(default_factory=set)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "raw_query": self.raw_query,
            "primary_domain": self.primary_domain,
            "action_type": self.action_type,
            "slots_needed": self.slots_needed,
            "requirements": [
                {
                    "slot": r.slot,
                    "description": r.description,
                    "preferred_tech": r.preferred_tech,
                    "negative_tech": r.negative_tech,
                    "critical": r.critical,
                }
                for r in self.requirements
            ],
            "explicit_mentions": sorted(list(self.explicit_mentions)),
            "constraints": self.constraints,
            "negative_preferences": sorted(list(self.negative_preferences)),
        }


IntentSpec = AnalyzedIntent


# Capability dictionary mapping technologies and patterns to canonical capability slots
SLOT_PATTERNS: Dict[str, Dict[str, Any]] = {
    "frontend": {
        "keywords": ["frontend", "ui", "ux", "react", "vue", "angular", "svelte", "nextjs", "tailwind", "html", "css", "web app", "dashboard", "interface"],
        "tech_map": {
            "react": ["react", "reactjs", "nextjs", "next.js"],
            "vue": ["vue", "vuejs", "nuxt"],
            "angular": ["angular"],
            "svelte": ["svelte", "sveltekit"],
            "tailwind": ["tailwind", "tailwindcss"],
        },
        "default_skill": "frontend-engineering",
    },
    "database": {
        "keywords": ["database", "db", "sql", "nosql", "postgres", "postgresql", "mysql", "sqlite", "mongodb", "redis", "prisma", "drizzle", "orm", "storage", "data store"],
        "tech_map": {
            "postgresql": ["postgres", "postgresql", "psql"],
            "mysql": ["mysql"],
            "sqlite": ["sqlite", "sqlite3"],
            "mongodb": ["mongo", "mongodb"],
            "redis": ["redis", "cache"],
            "prisma": ["prisma"],
            "drizzle": ["drizzle"],
        },
        "default_skill": "database-design",
    },
    "authentication": {
        "keywords": ["auth", "authentication", "login", "signup", "oauth", "jwt", "session", "sso", "rbac", "permissions", "user account", "next-auth", "clerk", "supabase auth"],
        "tech_map": {
            "oauth": ["oauth", "oauth2", "oidc"],
            "jwt": ["jwt", "tokens"],
            "next-auth": ["next-auth", "nextauth", "authjs"],
            "clerk": ["clerk"],
            "cognito": ["cognito"],
        },
        "default_skill": "iam-zero-trust-identity",
    },
    "payments": {
        "keywords": ["payment", "payments", "stripe", "paypal", "billing", "checkout", "subscription", "pricing", "invoicing", "e-commerce", "ecommerce"],
        "tech_map": {
            "stripe": ["stripe"],
            "paypal": ["paypal"],
            "paddle": ["paddle"],
            "lemonsqueezy": ["lemon", "lemonsqueezy"],
        },
        "default_skill": "fintech-payment-gateways",
    },
    "backend": {
        "keywords": ["backend", "api", "rest", "graphql", "server", "endpoint", "fastapi", "express", "django", "flask", "nest", "spring", "grpc", "microservice"],
        "tech_map": {
            "fastapi": ["fastapi", "python api"],
            "express": ["express", "node api"],
            "django": ["django"],
            "flask": ["flask"],
            "graphql": ["graphql", "apollo"],
            "grpc": ["grpc", "protobuf"],
        },
        "default_skill": "api-and-interface-design",
    },
    "security": {
        "keywords": ["security", "secure", "vulnerability", "audit", "sast", "dast", "owasp", "sanitization", "xss", "csrf", "sqli", "penetration", "hardening"],
        "tech_map": {
            "stride": ["stride", "threat model"],
            "sast": ["sast", "static analysis"],
            "owasp": ["owasp", "top10"],
        },
        "default_skill": "security-sandboxing-guardrails",
    },
    "testing": {
        "keywords": ["test", "tests", "testing", "unit test", "integration test", "e2e", "jest", "pytest", "playwright", "cypress", "tdd", "qa"],
        "tech_map": {
            "playwright": ["playwright"],
            "cypress": ["cypress"],
            "pytest": ["pytest"],
            "jest": ["jest"],
            "tdd": ["tdd", "test driven"],
        },
        "default_skill": "tdd",
    },
    "deployment": {
        "keywords": ["deploy", "deployment", "docker", "kubernetes", "k8s", "ci/cd", "github actions", "aws", "gcp", "azure", "cloud", "serverless", "terraform", "infra"],
        "tech_map": {
            "docker": ["docker", "container"],
            "kubernetes": ["kubernetes", "k8s"],
            "terraform": ["terraform"],
            "aws": ["aws", "lambda", "ecs"],
            "gcp": ["gcp", "google cloud"],
            "azure": ["azure"],
        },
        "default_skill": "cloud-devops",
    },
    "observability": {
        "keywords": ["metrics", "monitoring", "logging", "tracing", "prometheus", "grafana", "opentelemetry", "datadog", "sre", "apm", "alerting"],
        "tech_map": {
            "prometheus": ["prometheus", "promql"],
            "grafana": ["grafana"],
            "opentelemetry": ["opentelemetry", "otel"],
        },
        "default_skill": "metrics-alerting-prometheus-grafana",
    },
}

ACTION_KEYWORDS = {
    "build": ["build", "create", "scaffold", "implement", "develop", "make", "new"],
    "debug": ["debug", "fix", "resolve", "bug", "error", "failing", "broken", "issue"],
    "audit": ["audit", "inspect", "review", "evaluate", "assess", "check", "scan"],
    "optimize": ["optimize", "tune", "speed up", "performance", "profiling", "fast"],
    "migrate": ["migrate", "upgrade", "port", "convert", "transition"],
    "test": ["test", "verify", "benchmark", "validate"],
}


class IntentAnalyzer:
    """Analyzes a natural language user query into structured requirements."""

    def __init__(self) -> None:
        self.slot_defs = SLOT_PATTERNS

    def analyze(self, query: str) -> AnalyzedIntent:
        """Parse natural language request into domain, slots, and requirements."""
        q_lower = query.lower()
        words = re.findall(r"\b[a-z0-9_-]+\b", q_lower)
        word_set = set(words)

        # 1. Determine action type
        action_type = "build"
        for act, act_words in ACTION_KEYWORDS.items():
            if any(w in word_set for w in act_words):
                action_type = act
                break

        # 2. Extract negative preferences (e.g. "without docker", "no mongo", "never use next-auth")
        negatives = set()
        neg_patterns = [
            r"(?:without|no|not|never use|don't use|dont use|avoid)\s+([a-z0-9_-]+)",
        ]
        for pat in neg_patterns:
            matches = re.findall(pat, q_lower)
            for m in matches:
                negatives.add(m)

        # 3. Identify slots needed and map specific technologies
        slots_detected: List[str] = []
        requirements: List[IntentRequirement] = []
        explicit_mentions: Set[str] = set()

        for slot, conf in self.slot_defs.items():
            matched_keywords = [k for k in conf["keywords"] if k in q_lower]
            if not matched_keywords:
                continue

            slots_detected.append(slot)
            preferred: List[str] = []
            slot_negatives: List[str] = []

            # Check tech map
            for tech_canonical, aliases in conf["tech_map"].items():
                if any(alias in q_lower for alias in aliases):
                    if tech_canonical in negatives:
                        slot_negatives.append(tech_canonical)
                    else:
                        preferred.append(tech_canonical)
                        explicit_mentions.add(tech_canonical)

            # Check if any negative was found for this slot
            for neg in negatives:
                if neg in conf["tech_map"] and neg not in slot_negatives:
                    slot_negatives.append(neg)

            requirements.append(
                IntentRequirement(
                    slot=slot,
                    description=f"{slot.capitalize()} capability for {', '.join(preferred) if preferred else 'standard setup'}",
                    preferred_tech=preferred,
                    negative_tech=slot_negatives,
                    critical=(slot in ["frontend", "backend", "database", "payments"] if "build" in action_type else True),
                )
            )

        # 4. If no specific slots detected, default based on domain keywords
        if not slots_detected:
            slots_detected = ["backend"]
            requirements.append(
                IntentRequirement(
                    slot="backend",
                    description="General software engineering execution",
                    critical=True,
                )
            )

        # 5. Determine primary domain
        primary_domain = slots_detected[0] if slots_detected else "software-engineering"
        if "payments" in slots_detected:
            primary_domain = "fintech"
        elif "security" in slots_detected and action_type in ("audit", "debug"):
            primary_domain = "security"
        elif "frontend" in slots_detected:
            primary_domain = "web"

        return AnalyzedIntent(
            raw_query=query,
            primary_domain=primary_domain,
            action_type=action_type,
            slots_needed=slots_detected,
            requirements=requirements,
            explicit_mentions=explicit_mentions,
            constraints={"strict_security": "payments" in slots_detected or "security" in slots_detected},
            negative_preferences=negatives,
        )
