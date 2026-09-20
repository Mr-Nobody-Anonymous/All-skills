"""
Skill-Lifx Skill Package.
"""

from .skill import LifxSkill

def create_skill():
    return LifxSkill()

__all__ = ["LifxSkill", "create_skill"]
