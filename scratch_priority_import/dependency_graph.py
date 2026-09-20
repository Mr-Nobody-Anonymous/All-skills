"""
Dependency Graph Engine for All-Skills.
Constructs, manages, and queries directed dependency graphs of skills.
"""

from typing import Dict, List, Set, Optional, Tuple
from collections import defaultdict, deque
import logging

logger = logging.getLogger(__name__)


class DependencyGraph:
    """Directed dependency graph where an edge A -> B indicates A depends on B."""

    def __init__(self):
        # adj[u] = set of nodes that u depends on
        self._dependencies: Dict[str, Set[str]] = defaultdict(set)
        # rev_adj[u] = set of nodes that depend on u (dependents / reverse edges)
        self._dependents: Dict[str, Set[str]] = defaultdict(set)
        self._all_nodes: Set[str] = set()

    def add_node(self, node: str) -> None:
        """Register a node in the graph."""
        self._all_nodes.add(node)
        if node not in self._dependencies:
            self._dependencies[node] = set()
        if node not in self._dependents:
            self._dependents[node] = set()

    def add_dependency(self, skill: str, depends_on: str) -> None:
        """Add directed edge: skill -> depends_on."""
        self.add_node(skill)
        self.add_node(depends_on)
        self._dependencies[skill].add(depends_on)
        self._dependents[depends_on].add(skill)

    def get_dependencies(self, skill: str) -> Set[str]:
        """Return direct dependencies of a skill."""
        return set(self._dependencies.get(skill, set()))

    def get_dependents(self, skill: str) -> Set[str]:
        """Return skills that directly depend on the specified skill."""
        return set(self._dependents.get(skill, set()))

    def get_all_dependencies(self, skill: str) -> Set[str]:
        """Return transitive closure of all dependencies (ancestors)."""
        visited = set()
        queue = deque(self.get_dependencies(skill))
        while queue:
            curr = queue.popleft()
            if curr not in visited:
                visited.add(curr)
                for dep in self.get_dependencies(curr):
                    if dep not in visited:
                        queue.append(dep)
        return visited

    def get_all_dependents(self, skill: str) -> Set[str]:
        """Return transitive closure of all dependents (descendants)."""
        visited = set()
        queue = deque(self.get_dependents(skill))
        while queue:
            curr = queue.popleft()
            if curr not in visited:
                visited.add(curr)
                for dep in self.get_dependents(curr):
                    if dep not in visited:
                        queue.append(dep)
        return visited

    def nodes(self) -> Set[str]:
        """Return all nodes in the graph."""
        return set(self._all_nodes)

    def in_degree(self, skill: str) -> int:
        """Number of skills that depend on this skill."""
        return len(self._dependents.get(skill, set()))

    def out_degree(self, skill: str) -> int:
        """Number of skills this skill depends on."""
        return len(self._dependencies.get(skill, set()))

    def to_dict(self) -> Dict[str, List[str]]:
        """Export adjacency mapping as dictionary."""
        return {node: sorted(list(self._dependencies[node])) for node in sorted(self._all_nodes)}
