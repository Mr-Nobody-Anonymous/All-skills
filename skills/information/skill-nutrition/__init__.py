"""
Skill-Nutrition Skill Package.
"""

from .skill import NutritionSkill

def create_skill():
    return NutritionSkill()

__all__ = ["NutritionSkill", "create_skill"]
