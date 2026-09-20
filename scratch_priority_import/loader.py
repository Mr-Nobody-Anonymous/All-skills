"""
Skill Loader - Loads and initializes skill modules
"""

import importlib
import importlib.util
import logging
import time
from typing import Any, Dict, List, Optional, Callable
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from .registry import SkillRegistry, SkillModule, SkillDomain, SkillLevel
from .priority import PriorityManager
from .resolver import DependencyResolver

logger = logging.getLogger(__name__)


class SkillLoader:
    """Main skill loader - orchestrates loading of all skill modules"""
    
    def __init__(self, 
                 skills_root: Optional[str] = None,
                 registry: Optional[SkillRegistry] = None,
                 max_workers: int = 4):
        self.skills_root = Path(skills_root) if skills_root else Path(__file__).parent.parent / "skills"
        self.registry = registry or SkillRegistry()
        self.priority_manager = PriorityManager(self.registry)
        self.resolver = DependencyResolver(self.registry)
        self.max_workers = max_workers
        self._hooks: Dict[str, List[Callable]] = {
            'pre_load': [],
            'post_load': [],
            'on_error': [],
        }
        self._load_times: Dict[str, float] = {}
    
    def add_hook(self, event: str, callback: Callable) -> None:
        """Add a hook for load events"""
        if event in self._hooks:
            self._hooks[event].append(callback)
    
    def discover_skills(self) -> List[SkillModule]:
        """Auto-discover skill modules from the skills directory"""
        discovered = []
        
        if not self.skills_root.exists():
            logger.warning(f"Skills root not found: {self.skills_root}")
            return discovered
        
        for domain_dir in self.skills_root.iterdir():
            if not domain_dir.is_dir() or domain_dir.name.startswith('_'):
                continue
            
            # Try to map directory name to domain enum
            try:
                domain = SkillDomain(domain_dir.name)
            except ValueError:
                logger.debug(f"Non-enum domain directory: {domain_dir.name}")
                continue
            
            for skill_file in domain_dir.rglob("*.py"):
                if skill_file.name.startswith('_'):
                    continue
                
                skill_name = skill_file.stem
                try:
                    rel_p = skill_file.relative_to(self.skills_root.parent)
                    module_path = str(rel_p).replace('/', '.').replace('\\', '.').rstrip('.py')
                except Exception:
                    module_path = ""
                
                skill = SkillModule(
                    name=f"{domain.value}.{skill_name}",
                    domain=domain,
                    level=SkillLevel.INTERMEDIATE,
                    priority=50,
                    module_path=module_path,
                )
                discovered.append(skill)
        
        logger.info(f"Discovered {len(discovered)} skills")
        return discovered
    
    def register_all_default_skills(self) -> None:
        """Register the default/built-in skill catalog"""
        from .catalog import get_full_catalog
        skills = get_full_catalog()
        self.registry.register_batch(skills)
        logger.info(f"Registered {len(skills)} default skills")
    
    def load_skill(self, skill_name: str, force: bool = False) -> bool:
        """Load a single skill and its dependencies"""
        skill = self.registry.get(skill_name)
        if not skill:
            logger.error(f"Skill '{skill_name}' not found in registry")
            return False
        
        if skill.loaded and not force:
            logger.debug(f"Skill '{skill_name}' already loaded")
            return True
        
        # Resolve dependencies first
        try:
            load_order = self.resolver.resolve(skill_name)
        except Exception as e:
            logger.error(f"Failed to resolve dependencies for '{skill_name}': {e}")
            self._trigger_hooks('on_error', skill, e)
            return False
        
        # Load in order
        for name in load_order:
            dep_skill = self.registry.get(name)
            if dep_skill and not dep_skill.loaded:
                success = self._load_single(dep_skill)
                if not success:
                    logger.error(f"Failed to load dependency '{name}' for '{skill_name}'")
                    return False
        
        return True
    
    def load_domain(self, domain: SkillDomain) -> Dict[str, bool]:
        """Load all skills in a domain"""
        skills = self.registry.get_by_domain(domain)
        results = {}
        
        self.priority_manager.compute_load_order()
        
        for skill in sorted(skills, key=lambda s: s.priority):
            results[skill.name] = self.load_skill(skill.name)
        
        return results
    
    def load_all(self, parallel: bool = False) -> Dict[str, bool]:
        """Load all registered skills"""
        load_order = self.priority_manager.compute_load_order()
        results = {}
        
        if parallel:
            results = self._load_parallel(load_order)
        else:
            for skill_name in load_order:
                results[skill_name] = self.load_skill(skill_name)
        
        loaded = sum(1 for v in results.values() if v)
        total = len(results)
        logger.info(f"Loaded {loaded}/{total} skills")
        
        return results
    
    def _load_single(self, skill: SkillModule) -> bool:
        """Internal: Load a single skill module"""
        start_time = time.time()
        
        # Pre-load hooks
        self._trigger_hooks('pre_load', skill)
        
        try:
            if skill.module_path:
                try:
                    module = importlib.import_module(skill.module_path)
                    self.registry._loaded_modules[skill.name] = module
                    if hasattr(module, 'setup'):
                        module.setup()
                except Exception as ex:
                    logger.debug(f"Module import skipped for {skill.name}: {ex}")
            
            skill.loaded = True
            elapsed = time.time() - start_time
            self._load_times[skill.name] = elapsed
            
            # Post-load hooks
            self._trigger_hooks('post_load', skill)
            
            logger.info(f"Loaded '{skill.name}' in {elapsed:.3f}s")
            return True
            
        except Exception as e:
            logger.error(f"Error loading '{skill.name}': {e}")
            self._trigger_hooks('on_error', skill, e)
            return False
    
    def _load_parallel(self, load_order: List[str]) -> Dict[str, bool]:
        """Load skills in parallel where possible"""
        results = {}
        levels = self._group_by_dependency_level(load_order)
        
        for level_skills in levels:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                futures = {}
                for name in level_skills:
                    skill = self.registry.get(name)
                    if skill:
                        futures[executor.submit(self._load_single, skill)] = name
                
                for future in as_completed(futures):
                    name = futures[future]
                    try:
                        results[name] = future.result()
                    except Exception as e:
                        results[name] = False
                        logger.error(f"Parallel load error for '{name}': {e}")
        
        return results
    
    def _group_by_dependency_level(self, load_order: List[str]) -> List[List[str]]:
        """Group skills by dependency level for parallel loading"""
        levels = []
        loaded = set()
        remaining = list(load_order)
        
        while remaining:
            current_level = []
            for name in remaining[:]:
                skill = self.registry.get(name)
                if skill and all(dep in loaded for dep in skill.dependencies):
                    current_level.append(name)
            
            if not current_level:
                current_level = remaining[:]
            
            for name in current_level:
                remaining.remove(name)
                loaded.add(name)
            
            levels.append(current_level)
        
        return levels
    
    def _trigger_hooks(self, event: str, skill: SkillModule, error: Exception = None):
        """Trigger registered hooks"""
        for callback in self._hooks.get(event, []):
            try:
                if error:
                    callback(skill, error)
                else:
                    callback(skill)
            except Exception as e:
                logger.error(f"Hook error ({event}): {e}")
    
    def get_load_report(self) -> Dict[str, Any]:
        """Get a detailed loading report"""
        return {
            "registry_stats": self.registry.stats(),
            "load_times": dict(sorted(
                self._load_times.items(), 
                key=lambda x: x[1], 
                reverse=True
            )),
            "total_load_time": sum(self._load_times.values()),
            "missing_dependencies": self.priority_manager.validate_dependencies(),
            "cycles": self.resolver.find_cycles(),
            "orphans": self.resolver.get_orphans(),
        }
