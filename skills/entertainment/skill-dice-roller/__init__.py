"""
Skill-Dice-Roller Skill Package.
"""

from .skill import DiceRollerSkill

def create_skill():
    return DiceRollerSkill()

__all__ = ["DiceRollerSkill", "create_skill"]
