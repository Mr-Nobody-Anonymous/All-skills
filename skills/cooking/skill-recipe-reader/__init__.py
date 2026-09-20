"""
Skill-Recipe-Reader Skill Package.
"""

from .skill import RecipeReaderSkill

def create_skill():
    return RecipeReaderSkill()

__all__ = ["RecipeReaderSkill", "create_skill"]
