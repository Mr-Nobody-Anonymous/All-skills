"""
Skill-Craft-Ideas Skill Package.
"""

from .skill import CraftIdeasSkill

def create_skill():
    return CraftIdeasSkill()

__all__ = ["CraftIdeasSkill", "create_skill"]
