"""
Skill-Tidal Skill Package.
"""

from .skill import TidalSkill

def create_skill():
    return TidalSkill()

__all__ = ["TidalSkill", "create_skill"]
