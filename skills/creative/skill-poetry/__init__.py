"""
Skill-Poetry Skill Package.
"""

from .skill import PoetrySkill

def create_skill():
    return PoetrySkill()

__all__ = ["PoetrySkill", "create_skill"]
