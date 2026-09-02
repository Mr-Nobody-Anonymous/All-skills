"""Named, deterministic skill chains.

Chains let a workflow be expressed explicitly in ``skills/chains.json`` instead
of relying purely on scoring-based composition to discover the same sequence
every time. The router can still suggest chains dynamically; this module makes
the canonical workflows reproducible.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional

from .registry import Registry


@dataclass(frozen=True)
class SkillChain:
    name: str
    description: str = ""
    steps: List[str] = field(default_factory=list)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    rationale: str = ""


class ChainStore:
    """In-memory index of named chains loaded from chains.json."""

    def __init__(self, chains: Dict[str, SkillChain]) -> None:
        self.chains = chains

    @classmethod
    def load(cls, chains_path: Path) -> "ChainStore":
        if not chains_path.exists():
            return cls({})
        try:
            data = json.loads(chains_path.read_text(encoding="utf-8"))
        except Exception:
            return cls({})
        chains: Dict[str, SkillChain] = {}
        for raw in data.get("chains", []):
            name = str(raw.get("name") or "").strip()
            if not name:
                continue
            chains[name] = SkillChain(
                name=name,
                description=str(raw.get("description") or ""),
                steps=[str(s).strip() for s in raw.get("steps", []) if str(s).strip()],
                inputs=[str(s).strip() for s in raw.get("inputs", []) if str(s).strip()],
                outputs=[str(s).strip() for s in raw.get("outputs", []) if str(s).strip()],
                rationale=str(raw.get("rationale") or ""),
            )
        return cls(chains)

    def get(self, name: str) -> Optional[SkillChain]:
        return self.chains.get(name)

    def names(self) -> List[str]:
        return sorted(self.chains.keys())

    def all(self) -> List[SkillChain]:
        return [self.chains[name] for name in self.names()]


def load_chains(workspace_root: Path) -> ChainStore:
    """Load named chains from ``<workspace_root>/skills/chains.json``."""
    return ChainStore.load(workspace_root / "skills" / "chains.json")


class ChainResolver:
    """Resolves a named chain against a live registry."""

    def __init__(self, registry: Registry) -> None:
        self.registry = registry

    def unresolved_steps(self, chain: SkillChain) -> List[str]:
        return [step for step in chain.steps if self.registry.get(step) is None]

    def resolve(self, chain: SkillChain) -> List[dict]:
        return [
            {"id": step, "description": self.registry.get(step).description}
            for step in chain.steps
            if self.registry.get(step) is not None
        ]

    def permission_summary(self, chain: SkillChain) -> List[dict]:
        summary: List[dict] = []
        for step in chain.steps:
            entry = self.registry.get(step)
            if not entry:
                continue
            summary.append(
                {
                    "id": step,
                    "permissions": entry.permissions or {},
                    "risk": entry.risk,
                    "lifecycle": entry.lifecycle,
                }
            )
        return summary