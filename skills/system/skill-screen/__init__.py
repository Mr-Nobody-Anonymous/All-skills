"""
Skill-Screen Skill Package.
"""

from .skill import ScreenSkill

def create_skill():
    return ScreenSkill()

__all__ = ["ScreenSkill", "create_skill"]
