"""
Skill-Food-Safety Skill Package.
"""

from .skill import FoodSafetySkill

def create_skill():
    return FoodSafetySkill()

__all__ = ["FoodSafetySkill", "create_skill"]
