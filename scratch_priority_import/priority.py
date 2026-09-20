"""
Priority Manager - Handles skill loading priorities and ordering
"""

import logging
from typing import Dict, List, Set, Tuple, Optional
from .registry import SkillRegistry, SkillModule, SkillLevel

logger = logging.getLogger(__name__)


class PriorityManager:
    """Manages skill loading priorities"""
    
    # Default priority weights by level
    LEVEL_WEIGHTS = {
        SkillLevel.FUNDAMENTAL: 0,
        SkillLevel.CORE: 100,
        SkillLevel.INTERMEDIATE: 200,
        SkillLevel.ADVANCED: 300,
        SkillLevel.EXPERT: 400,
        SkillLevel.SPECIALIZED: 500,
    }
    
    def __init__(self, registry: Optional[SkillRegistry] = None):
        self.registry = registry or SkillRegistry()
        self._custom_priorities: Dict[str, int] = {}
    
    def set_priority(self, skill_name: str, priority: int) -> None:
        """Set custom priority for a skill"""
        self._custom_priorities[skill_name] = priority
    
    def get_effective_priority(self, skill: SkillModule) -> int:
        """Calculate effective priority considering level and custom overrides"""
        if skill.name in self._custom_priorities:
            return self._custom_priorities[skill.name]
        return self.LEVEL_WEIGHTS.get(skill.level, 999) + skill.priority
    
    def compute_load_order(self) -> List[str]:
        """
        Compute the optimal load order based on:
        1. Dependencies (topological sort)
        2. Priority levels
        3. Custom priorities
        """
        all_skills = self.registry.get_all()
        
        # Build dependency graph
        graph: Dict[str, Set[str]] = {}
        in_degree: Dict[str, int] = {}
        
        for skill in all_skills:
            if not skill.enabled:
                continue
            graph.setdefault(skill.name, set())
            in_degree.setdefault(skill.name, 0)
            
            for dep in skill.dependencies:
                graph.setdefault(dep, set())
                graph[dep].add(skill.name)
                in_degree[skill.name] = in_degree.get(skill.name, 0) + 1
        
        # Kahn's algorithm with priority ordering
        # Start with nodes that have no dependencies
        available = []
        for name, degree in in_degree.items():
            if degree == 0:
                skill = self.registry.get(name)
                if skill:
                    available.append((self.get_effective_priority(skill), name))
        
        available.sort()  # Sort by priority
        
        load_order = []
        while available:
            # Take highest priority (lowest number)
            _, current = available.pop(0)
            load_order.append(current)
            
            # Update neighbors
            for neighbor in graph.get(current, set()):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    skill = self.registry.get(neighbor)
                    if skill:
                        available.append(
                            (self.get_effective_priority(skill), neighbor)
                        )
                        available.sort()
        
        # Check for cycles
        if len(load_order) != len([s for s in all_skills if s.enabled]):
            # Find skills involved in cycles
            loaded_set = set(load_order)
            cycled = [
                s.name for s in all_skills 
                if s.enabled and s.name not in loaded_set
            ]
            logger.error(
                f"Circular dependency detected involving: {cycled}"
            )
            # Still add them at the end
            load_order.extend(cycled)
        
        self.registry.set_load_order(load_order)
        logger.info(f"Computed load order for {len(load_order)} skills")
        return load_order
    
    def get_critical_path(self, target: str) -> List[str]:
        """Get the critical path (all dependencies) to load a target skill"""
        visited = set()
        path = []
        
        def dfs(name: str):
            if name in visited:
                return
            visited.add(name)
            skill = self.registry.get(name)
            if skill:
                for dep in skill.dependencies:
                    dfs(dep)
                path.append(name)
        
        dfs(target)
        return path
    
    def validate_dependencies(self) -> List[Tuple[str, str]]:
        """Validate all dependencies exist. Returns list of (skill, missing_dep)"""
        missing = []
        for skill in self.registry.get_all():
            for dep in skill.dependencies:
                if not self.registry.get(dep):
                    missing.append((skill.name, dep))
                    logger.warning(
                        f"Skill '{skill.name}' depends on "
                        f"'{dep}' which is not registered"
                    )
        return missing
