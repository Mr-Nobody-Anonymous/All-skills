"""
Skill-Rock-Paper-Scissors Skill Package.
"""

from .skill import RockPaperScissorsSkill

def create_skill():
    return RockPaperScissorsSkill()

__all__ = ["RockPaperScissorsSkill", "create_skill"]
