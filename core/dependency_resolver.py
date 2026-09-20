"""
Core Dependency Resolver.
Orchestrates dependency resolution across all core subsystems.
"""

from typing import List, Dict, Set, Optional
from scratch_priority_import.dependency_graph import DependencyGraph
from scratch_priority_import.circular_dependency_detector import CircularDependencyDetector
from scratch_priority_import.skill_registry import SkillRegistry


class DependencyResolver:
    """Core layer dependency resolver."""

    def __init__(self, registry: Optional[SkillRegistry] = None):
        self.registry = registry or SkillRegistry()
        self.graph = DependencyGraph()
        self.detector = CircularDependencyDetector(self.graph)

    def resolve(self, skill_name: str) -> List[str]:
        """Resolve load order for a skill and all of its dependencies."""
        deps = self.graph.get_all_dependencies(skill_name)
        # Topological sort
        visited = set()
        order = []

        def visit(n: str):
            if n in visited:
                return
            for d in sorted(self.graph.get_dependencies(n)):
                visit(d)
            visited.add(n)
            order.append(n)

        for d in sorted(deps):
            visit(d)
        visit(skill_name)
        return order
