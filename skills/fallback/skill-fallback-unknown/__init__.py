"""
Skill-Fallback-Unknown Skill Package.
"""

from .skill import FallbackUnknownSkill

def create_skill():
    return FallbackUnknownSkill()

__all__ = ["FallbackUnknownSkill", "create_skill"]
