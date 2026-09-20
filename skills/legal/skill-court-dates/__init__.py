"""
Skill-Court-Dates Skill Package.
"""

from .skill import CourtDatesSkill

def create_skill():
    return CourtDatesSkill()

__all__ = ["CourtDatesSkill", "create_skill"]
