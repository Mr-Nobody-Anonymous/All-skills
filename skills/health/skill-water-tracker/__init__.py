"""
Skill-Water-Tracker Skill Package.
"""

from .skill import WaterTrackerSkill

def create_skill():
    return WaterTrackerSkill()

__all__ = ["WaterTrackerSkill", "create_skill"]
