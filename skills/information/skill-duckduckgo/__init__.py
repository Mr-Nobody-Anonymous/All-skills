"""
Skill-Duckduckgo Skill Package.
"""

from .skill import DuckduckgoSkill

def create_skill():
    return DuckduckgoSkill()

__all__ = ["DuckduckgoSkill", "create_skill"]
