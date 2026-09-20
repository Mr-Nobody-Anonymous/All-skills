"""
Skill-Sign-Language Skill Package.
"""

from .skill import SignLanguageSkill

def create_skill():
    return SignLanguageSkill()

__all__ = ["SignLanguageSkill", "create_skill"]
