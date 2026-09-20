"""
Skill-Color-Info Skill Package.
"""

from .skill import ColorInfoSkill

def create_skill():
    return ColorInfoSkill()

__all__ = ["ColorInfoSkill", "create_skill"]
