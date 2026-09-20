"""
Skill-History-Tutor Skill Package.
"""

from .skill import HistoryTutorSkill

def create_skill():
    return HistoryTutorSkill()

__all__ = ["HistoryTutorSkill", "create_skill"]
