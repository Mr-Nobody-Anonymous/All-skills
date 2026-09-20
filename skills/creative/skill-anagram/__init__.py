"""
Skill-Anagram Skill Package.
"""

from .skill import AnagramSkill

def create_skill():
    return AnagramSkill()

__all__ = ["AnagramSkill", "create_skill"]
