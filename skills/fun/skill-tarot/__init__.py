"""
Skill-Tarot Skill Package.
"""

from .skill import TarotSkill

def create_skill():
    return TarotSkill()

__all__ = ["TarotSkill", "create_skill"]
