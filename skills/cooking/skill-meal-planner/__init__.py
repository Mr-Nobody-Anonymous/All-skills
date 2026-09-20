"""
Skill-Meal-Planner Skill Package.
"""

from .skill import MealPlannerSkill

def create_skill():
    return MealPlannerSkill()

__all__ = ["MealPlannerSkill", "create_skill"]
