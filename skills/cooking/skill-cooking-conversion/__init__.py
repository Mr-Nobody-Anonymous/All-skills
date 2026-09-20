"""
Skill-Cooking-Conversion Skill Package.
"""

from .skill import CookingConversionSkill

def create_skill():
    return CookingConversionSkill()

__all__ = ["CookingConversionSkill", "create_skill"]
