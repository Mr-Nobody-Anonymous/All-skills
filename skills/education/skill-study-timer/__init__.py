"""
Skill-Study-Timer Skill Package.
"""

from .skill import StudyTimerSkill

def create_skill():
    return StudyTimerSkill()

__all__ = ["StudyTimerSkill", "create_skill"]
