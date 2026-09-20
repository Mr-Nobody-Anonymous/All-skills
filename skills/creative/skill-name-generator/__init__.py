"""
Skill-Name-Generator Skill Package.
"""

from .skill import NameGeneratorSkill

def create_skill():
    return NameGeneratorSkill()

__all__ = ["NameGeneratorSkill", "create_skill"]
