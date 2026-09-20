"""
Skill-Bbc-News Skill Package.
"""

from .skill import BbcNewsSkill

def create_skill():
    return BbcNewsSkill()

__all__ = ["BbcNewsSkill", "create_skill"]
