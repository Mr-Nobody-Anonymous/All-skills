"""
Skill-Astronomy Skill Package.
"""

from .skill import AstronomySkill

def create_skill():
    return AstronomySkill()

__all__ = ["AstronomySkill", "create_skill"]
