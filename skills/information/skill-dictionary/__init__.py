"""
Skill-Dictionary Skill Package.
"""

from .skill import DictionarySkill

def create_skill():
    return DictionarySkill()

__all__ = ["DictionarySkill", "create_skill"]
