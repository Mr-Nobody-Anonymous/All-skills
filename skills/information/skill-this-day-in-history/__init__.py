"""
Skill-This-Day-In-History Skill Package.
"""

from .skill import ThisDayInHistorySkill

def create_skill():
    return ThisDayInHistorySkill()

__all__ = ["ThisDayInHistorySkill", "create_skill"]
