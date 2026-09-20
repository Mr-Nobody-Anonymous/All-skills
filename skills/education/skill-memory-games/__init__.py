"""
Skill-Memory-Games Skill Package.
"""

from .skill import MemoryGamesSkill

def create_skill():
    return MemoryGamesSkill()

__all__ = ["MemoryGamesSkill", "create_skill"]
