"""
Skill-Ice-Breakers Skill Package.
"""

from .skill import IceBreakersSkill

def create_skill():
    return IceBreakersSkill()

__all__ = ["IceBreakersSkill", "create_skill"]
