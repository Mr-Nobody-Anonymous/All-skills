"""
Skill-Screen-Cast Skill Package.
"""

from .skill import ScreenCastSkill

def create_skill():
    return ScreenCastSkill()

__all__ = ["ScreenCastSkill", "create_skill"]
