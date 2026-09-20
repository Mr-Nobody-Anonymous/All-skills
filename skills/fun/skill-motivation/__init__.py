"""
Skill-Motivation Skill Package.
"""

from .skill import MotivationSkill

def create_skill():
    return MotivationSkill()

__all__ = ["MotivationSkill", "create_skill"]
