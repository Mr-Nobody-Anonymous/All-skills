"""
Skill-Visual Skill Package.
"""

from .skill import VisualSkill

def create_skill():
    return VisualSkill()

__all__ = ["VisualSkill", "create_skill"]
