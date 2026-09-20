"""
Skill-Translator Skill Package.
"""

from .skill import TranslatorSkill

def create_skill():
    return TranslatorSkill()

__all__ = ["TranslatorSkill", "create_skill"]
