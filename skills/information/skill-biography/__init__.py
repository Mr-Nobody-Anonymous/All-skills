"""
Skill-Biography Skill Package.
"""

from .skill import BiographySkill

def create_skill():
    return BiographySkill()

__all__ = ["BiographySkill", "create_skill"]
