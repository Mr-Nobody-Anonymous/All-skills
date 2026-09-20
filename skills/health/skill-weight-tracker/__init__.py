"""
Skill-Weight-Tracker Skill Package.
"""

from .skill import WeightTrackerSkill

def create_skill():
    return WeightTrackerSkill()

__all__ = ["WeightTrackerSkill", "create_skill"]
