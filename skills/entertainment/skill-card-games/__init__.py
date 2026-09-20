"""
Skill-Card-Games Skill Package.
"""

from .skill import CardGamesSkill

def create_skill():
    return CardGamesSkill()

__all__ = ["CardGamesSkill", "create_skill"]
