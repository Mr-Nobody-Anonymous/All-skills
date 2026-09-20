"""
Skill-Motor Skill Package.
"""

from .skill import MotorSkill

def create_skill():
    return MotorSkill()

__all__ = ["MotorSkill", "create_skill"]
