"""
Skill-Number-Games Skill Package.
"""

from .skill import NumberGamesSkill

def create_skill():
    return NumberGamesSkill()

__all__ = ["NumberGamesSkill", "create_skill"]
