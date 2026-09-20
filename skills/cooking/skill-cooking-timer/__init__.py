"""
Skill-Cooking-Timer Skill Package.
"""

from .skill import CookingTimerSkill

def create_skill():
    return CookingTimerSkill()

__all__ = ["CookingTimerSkill", "create_skill"]
