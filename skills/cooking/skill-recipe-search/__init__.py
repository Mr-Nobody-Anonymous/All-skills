"""
Skill-Recipe-Search Skill Package.
"""

from .skill import RecipeSearchSkill

def create_skill():
    return RecipeSearchSkill()

__all__ = ["RecipeSearchSkill", "create_skill"]
