"""
Skill-Tides Skill Package.
"""

from .skill import TidesSkill

def create_skill():
    return TidesSkill()

__all__ = ["TidesSkill", "create_skill"]
