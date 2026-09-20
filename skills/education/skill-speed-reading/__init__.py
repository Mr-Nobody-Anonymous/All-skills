"""
Skill-Speed-Reading Skill Package.
"""

from .skill import SpeedReadingSkill

def create_skill():
    return SpeedReadingSkill()

__all__ = ["SpeedReadingSkill", "create_skill"]
