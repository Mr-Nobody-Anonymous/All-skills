"""
Skill-Sprinkler Skill Package.
"""

from .skill import SprinklerSkill

def create_skill():
    return SprinklerSkill()

__all__ = ["SprinklerSkill", "create_skill"]
