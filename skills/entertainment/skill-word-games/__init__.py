"""
Skill-Word-Games Skill Package.
"""

from .skill import WordGamesSkill

def create_skill():
    return WordGamesSkill()

__all__ = ["WordGamesSkill", "create_skill"]
