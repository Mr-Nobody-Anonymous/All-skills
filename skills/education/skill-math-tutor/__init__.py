"""
Skill-Math-Tutor Skill Package.
"""

from .skill import MathTutorSkill

def create_skill():
    return MathTutorSkill()

__all__ = ["MathTutorSkill", "create_skill"]
