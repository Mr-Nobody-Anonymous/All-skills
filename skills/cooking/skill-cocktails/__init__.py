"""
Skill-Cocktails Skill Package.
"""

from .skill import CocktailsSkill

def create_skill():
    return CocktailsSkill()

__all__ = ["CocktailsSkill", "create_skill"]
