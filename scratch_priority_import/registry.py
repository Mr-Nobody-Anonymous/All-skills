"""
Skill Registry - Central registry for all skill modules
"""

import importlib
import logging
from typing import Dict, List, Optional, Any, Set
from dataclasses import dataclass, field
from enum import Enum, auto
from pathlib import Path

logger = logging.getLogger(__name__)


class SkillLevel(Enum):
    FUNDAMENTAL = auto()    # Must load first
    CORE = auto()           # Core skills, load second
    INTERMEDIATE = auto()   # Depends on core
    ADVANCED = auto()       # Depends on intermediate
    EXPERT = auto()         # Depends on advanced
    SPECIALIZED = auto()    # Domain-specific


class SkillDomain(Enum):
    PROGRAMMING = "programming"
    AI_ML = "ai_ml"
    CYBERSECURITY = "cybersecurity"
    WEB_DEV = "web_development"
    DEVOPS = "devops"
    DATA = "data_engineering"
    BLOCKCHAIN = "blockchain"
    MOBILE = "mobile_development"
    GAME_DEV = "game_development"
    EMBEDDED = "embedded_systems"
    OS_LOWLEVEL = "os_and_low_level"
    MATH_CS = "math_and_cs_theory"
    GRAPHICS_3D = "graphics_and_3d"
    NETWORKING = "networking"
    DESIGN = "design"
    AUDIO = "audio_and_music"
    ROBOTICS = "robotics"
    QUANTUM = "quantum_computing"
    BUSINESS = "business"
    SCIENCE = "science"
    CREATIVE = "creative_arts"
    LANGUAGES = "languages"
    HEALTH = "health_fitness"
    SURVIVAL = "survival_practical"
    PSYCHOLOGY = "psychology"
    LEGAL = "legal"
    AUTOMATION = "automation"
    PRIVACY = "privacy_anonymity"


@dataclass
class SkillModule:
    """Represents a single skill module"""
    name: str
    domain: SkillDomain
    level: SkillLevel
    priority: int  # 0 = highest priority
    dependencies: List[str] = field(default_factory=list)
    description: str = ""
    module_path: str = ""
    tags: List[str] = field(default_factory=list)
    resources: List[str] = field(default_factory=list)
    repos: List[str] = field(default_factory=list)
    loaded: bool = False
    enabled: bool = True
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        if isinstance(other, SkillModule):
            return self.name == other.name
        return False


class SkillRegistry:
    """Central registry for all skills"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        if getattr(self, "_initialized", False):
            return
        self._skills: Dict[str, SkillModule] = {}
        self._domains: Dict[SkillDomain, List[str]] = {
            domain: [] for domain in SkillDomain
        }
        self._loaded_modules: Dict[str, Any] = {}
        self._load_order: List[str] = []
        self._initialized = True
        logger.info("SkillRegistry initialized")
    
    def register(self, skill: SkillModule) -> None:
        """Register a skill module"""
        if skill.name in self._skills:
            logger.warning(f"Skill '{skill.name}' already registered, updating")
        self._skills[skill.name] = skill
        if skill.name not in self._domains[skill.domain]:
            self._domains[skill.domain].append(skill.name)
        logger.info(f"Registered skill: {skill.name} [{skill.domain.value}]")
    
    def register_batch(self, skills: List[SkillModule]) -> None:
        """Register multiple skills at once"""
        for skill in skills:
            self.register(skill)
    
    def get(self, name: str) -> Optional[SkillModule]:
        """Get a skill by name"""
        return self._skills.get(name)
    
    def get_by_domain(self, domain: SkillDomain) -> List[SkillModule]:
        """Get all skills in a domain"""
        return [self._skills[name] for name in self._domains.get(domain, [])]
    
    def get_by_level(self, level: SkillLevel) -> List[SkillModule]:
        """Get all skills at a certain level"""
        return [s for s in self._skills.values() if s.level == level]
    
    def get_by_tag(self, tag: str) -> List[SkillModule]:
        """Get all skills with a specific tag"""
        return [s for s in self._skills.values() if tag in s.tags]
    
    def get_dependencies(self, name: str) -> List[SkillModule]:
        """Get all dependencies for a skill"""
        skill = self._skills.get(name)
        if not skill:
            return []
        return [self._skills[dep] for dep in skill.dependencies if dep in self._skills]
    
    def get_all(self) -> List[SkillModule]:
        """Get all registered skills"""
        return list(self._skills.values())
    
    def get_load_order(self) -> List[str]:
        """Get the computed load order"""
        return self._load_order.copy()
    
    def set_load_order(self, order: List[str]) -> None:
        """Set the load order"""
        self._load_order = order
    
    def search(self, query: str) -> List[SkillModule]:
        """Search skills by name, description, or tags"""
        query = query.lower()
        results = []
        for skill in self._skills.values():
            if (query in skill.name.lower() or 
                query in skill.description.lower() or
                any(query in tag.lower() for tag in skill.tags)):
                results.append(skill)
        return results
    
    @property
    def count(self) -> int:
        return len(self._skills)
    
    @property
    def domain_counts(self) -> Dict[str, int]:
        return {
            domain.value: len(skills) 
            for domain, skills in self._domains.items()
        }
    
    def stats(self) -> Dict[str, Any]:
        """Get registry statistics"""
        return {
            "total_skills": self.count,
            "domains": self.domain_counts,
            "levels": {
                level.name: len(self.get_by_level(level))
                for level in SkillLevel
            },
            "loaded": sum(1 for s in self._skills.values() if s.loaded),
            "enabled": sum(1 for s in self._skills.values() if s.enabled),
        }
    
    def export_catalog(self) -> Dict[str, Any]:
        """Export full catalog as dictionary"""
        catalog = {}
        for domain in SkillDomain:
            skills = self.get_by_domain(domain)
            if skills:
                catalog[domain.value] = [
                    {
                        "name": s.name,
                        "level": s.level.name,
                        "priority": s.priority,
                        "dependencies": s.dependencies,
                        "description": s.description,
                        "tags": s.tags,
                        "repos": s.repos,
                        "loaded": s.loaded,
                    }
                    for s in sorted(skills, key=lambda x: x.priority)
                ]
        return catalog
    
    def reset(self) -> None:
        """Reset the registry"""
        self._skills.clear()
        self._domains = {domain: [] for domain in SkillDomain}
        self._loaded_modules.clear()
        self._load_order.clear()
        logger.info("SkillRegistry reset")
