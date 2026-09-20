"""
Dependency Resolver - Resolves and validates skill dependencies
"""

import logging
from typing import Dict, List, Set, Optional, Tuple
from .registry import SkillRegistry, SkillModule

logger = logging.getLogger(__name__)


class CircularDependencyError(Exception):
    """Raised when a circular dependency is detected"""
    pass


class DependencyResolver:
    """Resolves skill dependencies and detects conflicts"""
    
    def __init__(self, registry: Optional[SkillRegistry] = None):
        self.registry = registry or SkillRegistry()
    
    def resolve(self, skill_name: str) -> List[str]:
        """
        Resolve all dependencies for a skill (recursive).
        Returns ordered list of skills to load.
        """
        resolved = []
        seen = set()
        
        def _resolve(name: str, chain: List[str]):
            if name in seen:
                return
            
            skill = self.registry.get(name)
            if not skill:
                logger.warning(f"Skill '{name}' not found in registry")
                return
            
            if name in chain:
                cycle = chain[chain.index(name):] + [name]
                raise CircularDependencyError(
                    f"Circular dependency detected: {' -> '.join(cycle)}"
                )
            
            chain.append(name)
            
            for dep in skill.dependencies:
                _resolve(dep, chain.copy())
            
            if name not in seen:
                seen.add(name)
                resolved.append(name)
        
        _resolve(skill_name, [])
        return resolved
    
    def resolve_multiple(self, skill_names: List[str]) -> List[str]:
        """Resolve dependencies for multiple skills"""
        all_resolved = []
        seen = set()
        
        for name in skill_names:
            for resolved_name in self.resolve(name):
                if resolved_name not in seen:
                    seen.add(resolved_name)
                    all_resolved.append(resolved_name)
        
        return all_resolved
    
    def find_cycles(self) -> List[List[str]]:
        """Find all circular dependencies in the registry"""
        cycles = []
        visited = set()
        rec_stack = set()
        
        def dfs(name: str, path: List[str]) -> None:
            visited.add(name)
            rec_stack.add(name)
            path.append(name)
            
            skill = self.registry.get(name)
            if not skill:
                return
            
            for dep in skill.dependencies:
                if dep not in visited:
                    dfs(dep, path.copy())
                elif dep in rec_stack:
                    cycle_start = path.index(dep) if dep in path else -1
                    if cycle_start >= 0:
                        cycle = path[cycle_start:] + [dep]
                        cycles.append(cycle)
            
            rec_stack.discard(name)
        
        for skill in self.registry.get_all():
            if skill.name not in visited:
                dfs(skill.name, [])
        
        return cycles
    
    def get_dependency_tree(self, skill_name: str, depth: int = -1) -> Dict:
        """Get dependency tree as nested dict"""
        def _tree(name: str, current_depth: int, visited: Set[str]) -> Dict:
            if depth >= 0 and current_depth > depth:
                return {"_truncated": True}
            
            if name in visited:
                return {"_circular_ref": name}
            
            visited.add(name)
            skill = self.registry.get(name)
            
            if not skill:
                return {"_missing": True}
            
            tree = {
                "name": name,
                "level": skill.level.name,
                "domain": skill.domain.value,
                "dependencies": {}
            }
            
            for dep in skill.dependencies:
                tree["dependencies"][dep] = _tree(
                    dep, current_depth + 1, visited.copy()
                )
            
            return tree
        
        return _tree(skill_name, 0, set())
    
    def get_reverse_dependencies(self, skill_name: str) -> List[str]:
        """Find all skills that depend on this skill"""
        dependents = []
        for skill in self.registry.get_all():
            if skill_name in skill.dependencies:
                dependents.append(skill.name)
        return dependents
    
    def get_orphans(self) -> List[str]:
        """Find skills with no dependencies and no dependents"""
        all_deps = set()
        all_dependents = set()
        
        for skill in self.registry.get_all():
            if skill.dependencies:
                all_dependents.add(skill.name)
                all_deps.update(skill.dependencies)
        
        return [
            s.name for s in self.registry.get_all()
            if s.name not in all_deps and s.name not in all_dependents
        ]
