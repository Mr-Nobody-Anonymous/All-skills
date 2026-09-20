"""
Skill-Dice Skill Package.
"""

from .skill import DiceSkill

def create_skill():
    return DiceSkill()

__all__ = ["DiceSkill", "create_skill"]
