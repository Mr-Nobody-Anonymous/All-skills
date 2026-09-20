"""
Skill-Meme-Generator Skill Package.
"""

from .skill import MemeGeneratorSkill

def create_skill():
    return MemeGeneratorSkill()

__all__ = ["MemeGeneratorSkill", "create_skill"]
