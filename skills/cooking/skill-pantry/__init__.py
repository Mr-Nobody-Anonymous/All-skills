"""
Skill-Pantry Skill Package.
"""

from .skill import PantrySkill

def create_skill():
    return PantrySkill()

__all__ = ["PantrySkill", "create_skill"]
