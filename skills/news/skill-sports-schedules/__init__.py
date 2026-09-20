"""
Skill-Sports-Schedules Skill Package.
"""

from .skill import SportsSchedulesSkill

def create_skill():
    return SportsSchedulesSkill()

__all__ = ["SportsSchedulesSkill", "create_skill"]
