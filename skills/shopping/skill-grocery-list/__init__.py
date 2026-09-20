"""
Skill-Grocery-List Skill Package.
"""

from .skill import GroceryListSkill

def create_skill():
    return GroceryListSkill()

__all__ = ["GroceryListSkill", "create_skill"]
