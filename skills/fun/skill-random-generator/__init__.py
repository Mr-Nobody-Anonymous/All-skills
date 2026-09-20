"""
Skill-Random-Generator Skill Package.
"""

from .skill import RandomGeneratorSkill

def create_skill():
    return RandomGeneratorSkill()

__all__ = ["RandomGeneratorSkill", "create_skill"]
