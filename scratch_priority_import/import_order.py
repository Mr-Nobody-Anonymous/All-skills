"""
Import Order Orchestrator for scratch_priority_import.
Calculates deterministic load and import ordering based on:
1. Priority tiers and numeric rank (1-100)
2. Prerequisite dependency topological order
3. Core foundations first (STT, TTS, intent engine) before consumer skills
"""

from typing import List, Dict, Any
from .priority_registry import PriorityRegistry, RegisteredSkill
from .dependency_resolver import DependencyResolver

class ImportOrder:
    def __init__(self, registry: PriorityRegistry):
        self.registry = registry
        self.resolver = DependencyResolver()

    def compute_import_schedule(self) -> List[RegisteredSkill]:
        """
        Computes the definitive import schedule.
        Combines topological order of dependencies with priority tier weighting.
        """
        skills = self.registry.get_all(enabled_only=True)
        for s in skills:
            self.resolver.add_skill(s.name, s.dependencies)

        topo_order = self.resolver.resolve_order()
        topo_rank = {name: idx for idx, name in enumerate(topo_order)}

        # Sort with topological order as primary key, numeric priority as tie-breaker
        sorted_skills = sorted(
            skills,
            key=lambda s: (topo_rank.get(s.name, 999), s.priority)
        )
        return sorted_skills

    def get_eager_skills(self) -> List[RegisteredSkill]:
        return [s for s in self.compute_import_schedule() if s.load_strategy == "eager"]

    def get_lazy_skills(self) -> List[RegisteredSkill]:
        return [s for s in self.compute_import_schedule() if s.load_strategy == "lazy"]
