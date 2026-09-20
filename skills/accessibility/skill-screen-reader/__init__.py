"""
Skill-Screen-Reader Skill Package.
"""

from .skill import ScreenReaderSkill

def create_skill():
    return ScreenReaderSkill()

__all__ = ["ScreenReaderSkill", "create_skill"]
