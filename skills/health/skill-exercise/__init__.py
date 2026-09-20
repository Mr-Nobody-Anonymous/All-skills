"""
Skill-Exercise Skill Package.
"""

from .skill import ExerciseSkill

def create_skill():
    return ExerciseSkill()

__all__ = ["ExerciseSkill", "create_skill"]
