"""
Skill-Baby-Names Skill Package.
"""

from .skill import BabyNamesSkill

def create_skill():
    return BabyNamesSkill()

__all__ = ["BabyNamesSkill", "create_skill"]
