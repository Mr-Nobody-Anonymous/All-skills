"""
Dependency Resolver for scratch_priority_import.
Constructs dependency trees between skills, resolves topological sorting,
and detects missing or broken prerequisite skills.
"""

from typing import Dict, List, Set, Optional

class DependencyResolver:
    def __init__(self):
        self.adj_list: Dict[str, List[str]] = {}

    def add_skill(self, skill_id: str, dependencies: Optional[List[str]] = None):
        if skill_id not in self.adj_list:
            self.adj_list[skill_id] = []
        if dependencies:
            self.adj_list[skill_id].extend(dependencies)

    def resolve_order(self) -> List[str]:
        """Returns topological load order such that dependencies load before consumers."""
        in_degree: Dict[str, int] = {node: 0 for node in self.adj_list}
        all_nodes = set(self.adj_list.keys())
        
        # Ensure referenced dependencies also have entries
        for deps in self.adj_list.values():
            for d in deps:
                if d not in in_degree:
                    in_degree[d] = 0

        for node, deps in self.adj_list.items():
            for dep in deps:
                in_degree[node] = in_degree.get(node, 0) + 1

        queue = [node for node, deg in in_degree.items() if deg == 0]
        order = []

        while queue:
            curr = queue.pop(0)
            order.append(curr)

            for node, deps in self.adj_list.items():
                if curr in deps:
                    in_degree[node] -= 1
                    if in_degree[node] == 0:
                        queue.append(node)

        # Append any remaining unvisited nodes
        for node in in_degree:
            if node not in order:
                order.append(node)

        return order

    def find_missing_dependencies(self, available_skills: Set[str]) -> Dict[str, List[str]]:
        """Identifies skills requiring dependencies that are not available."""
        missing = {}
        for skill, deps in self.adj_list.items():
            unmet = [d for d in deps if d not in available_skills]
            if unmet:
                missing[skill] = unmet
        return missing
