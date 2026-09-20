"""
Skill-Fallback-Duckduckgo Skill Package.
"""

from .skill import FallbackDuckduckgoSkill

def create_skill():
    return FallbackDuckduckgoSkill()

__all__ = ["FallbackDuckduckgoSkill", "create_skill"]
