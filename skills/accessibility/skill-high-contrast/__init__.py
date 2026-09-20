"""
Skill-High-Contrast Skill Package.
"""

from .skill import HighContrastSkill

def create_skill():
    return HighContrastSkill()

__all__ = ["HighContrastSkill", "create_skill"]
