"""
Skill-Battery Skill Package.
"""

from .skill import BatterySkill

def create_skill():
    return BatterySkill()

__all__ = ["BatterySkill", "create_skill"]
