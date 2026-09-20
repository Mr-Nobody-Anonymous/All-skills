"""
Skill-Sleep Skill Package.
"""

from .skill import SleepSkill

def create_skill():
    return SleepSkill()

__all__ = ["SleepSkill", "create_skill"]
