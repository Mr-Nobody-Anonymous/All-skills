"""
Skill-Blinds Skill Package.
"""

from .skill import BlindsSkill

def create_skill():
    return BlindsSkill()

__all__ = ["BlindsSkill", "create_skill"]
