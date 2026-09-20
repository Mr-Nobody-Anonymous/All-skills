"""
Configuration for the skill system
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, field


@dataclass
class SkillConfig:
    """Configuration for skill loading"""
    skills_root: str = "./skills"
    max_workers: int = 4
    auto_discover: bool = True
    load_on_init: bool = False
    log_level: str = "INFO"
    enabled_domains: list = field(default_factory=list)  # Empty = all
    disabled_skills: list = field(default_factory=list)
    custom_priorities: Dict[str, int] = field(default_factory=dict)
    
    @classmethod
    def from_file(cls, path: str) -> 'SkillConfig':
        """Load config from YAML or JSON file"""
        filepath = Path(path)
        
        if not filepath.exists():
            return cls()
        
        with open(filepath, "r", encoding="utf-8") as f:
            if filepath.suffix in ('.yml', '.yaml'):
                data = yaml.safe_load(f) or {}
            elif filepath.suffix == '.json':
                data = json.load(f)
            else:
                raise ValueError(f"Unsupported config format: {filepath.suffix}")
        
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
    
    def to_file(self, path: str) -> None:
        """Save config to file"""
        filepath = Path(path)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        data = {
            k: getattr(self, k) 
            for k in self.__dataclass_fields__
        }
        
        with open(filepath, 'w', encoding="utf-8") as f:
            if filepath.suffix in ('.yml', '.yaml'):
                yaml.dump(data, f, default_flow_style=False)
            else:
                json.dump(data, f, indent=2)
