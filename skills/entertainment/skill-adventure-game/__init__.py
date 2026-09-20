"""
Skill-Adventure-Game Skill Package.
"""

from .skill import AdventureGameSkill

def create_skill():
    return AdventureGameSkill()

__all__ = ["AdventureGameSkill", "create_skill"]
