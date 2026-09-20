"""
Skill-Coding-Tutorial Skill Package.
"""

from .skill import CodingTutorialSkill

def create_skill():
    return CodingTutorialSkill()

__all__ = ["CodingTutorialSkill", "create_skill"]
