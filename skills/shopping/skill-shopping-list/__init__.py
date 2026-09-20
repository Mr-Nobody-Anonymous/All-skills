"""
Skill-Shopping-List Skill Package.
"""

from .skill import ShoppingListSkill

def create_skill():
    return ShoppingListSkill()

__all__ = ["ShoppingListSkill", "create_skill"]
