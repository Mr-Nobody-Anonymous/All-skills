"""
Skill-Workout Skill Package.
"""

from .skill import WorkoutSkill

def create_skill():
    return WorkoutSkill()

__all__ = ["WorkoutSkill", "create_skill"]
