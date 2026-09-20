"""
Skill-Creative-Writing Skill Package.
"""

from .skill import CreativeWritingSkill

def create_skill():
    return CreativeWritingSkill()

__all__ = ["CreativeWritingSkill", "create_skill"]
