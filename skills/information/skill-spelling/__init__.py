"""
Skill-Spelling Skill Package.
"""

from .skill import SpellingSkill

def create_skill():
    return SpellingSkill()

__all__ = ["SpellingSkill", "create_skill"]
