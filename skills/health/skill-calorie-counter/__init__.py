"""
Skill-Calorie-Counter Skill Package.
"""

from .skill import CalorieCounterSkill

def create_skill():
    return CalorieCounterSkill()

__all__ = ["CalorieCounterSkill", "create_skill"]
