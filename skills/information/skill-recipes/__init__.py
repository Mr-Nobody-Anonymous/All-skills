"""
Skill-Recipes Skill Package.
"""

from .skill import RecipesSkill

def create_skill():
    return RecipesSkill()

__all__ = ["RecipesSkill", "create_skill"]
