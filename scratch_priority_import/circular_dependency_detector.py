"""
Circular Dependency Detector for All-Skills.
Detects, isolates, and reports circular references in skill dependency chains.
"""

from typing import Dict, List, Set, Optional
import logging

from .dependency_graph import DependencyGraph

logger = logging.getLogger(__name__)


class CircularDependencyError(Exception):
    """Raised when a circular dependency is detected."""
    def __init__(self, cycle: List[str]):
        self.cycle = cycle
        msg = f"Circular dependency detected: {' -> '.join(cycle)}"
        super().__init__(msg)


class CircularDependencyDetector:
    """Detects cycles in skill graphs using depth-first search with recursion tracking."""

    def __init__(self, graph: Optional[DependencyGraph] = None):
        self.graph = graph or DependencyGraph()

    def find_cycles(self, graph: Optional[DependencyGraph] = None) -> List[List[str]]:
        """Find all distinct elementary cycles in the dependency graph."""
        g = graph or self.graph
        visited: Set[str] = set()
        rec_stack: Set[str] = set()
        path: List[str] = []
        cycles: List[List[str]] = []

        def dfs(node: str) -> None:
            visited.add(node)
            rec_stack.add(node)
            path.append(node)

            for neighbor in g.get_dependencies(node):
                if neighbor not in visited:
                    dfs(neighbor)
                elif neighbor in rec_stack:
                    # Found cycle: slice path from neighbor to current
                    cycle_start = path.index(neighbor)
                    cycle = path[cycle_start:] + [neighbor]
                    cycles.append(cycle)

            path.pop()
            rec_stack.remove(node)

        for node in sorted(g.nodes()):
            if node not in visited:
                dfs(node)

        return cycles

    def validate(self, graph: Optional[DependencyGraph] = None) -> None:
        """Validate that no cycles exist. Raises CircularDependencyError if found."""
        cycles = self.find_cycles(graph)
        if cycles:
            first_cycle = cycles[0]
            raise CircularDependencyError(first_cycle)

    def has_cycle(self, graph: Optional[DependencyGraph] = None) -> bool:
        """Return True if any cycle is detected, False otherwise."""
        return len(self.find_cycles(graph)) > 0
