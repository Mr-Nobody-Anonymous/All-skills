"""
Skill-Fitness-Tracker Skill Package.
"""

from .skill import FitnessTrackerSkill

def create_skill():
    return FitnessTrackerSkill()

__all__ = ["FitnessTrackerSkill", "create_skill"]
