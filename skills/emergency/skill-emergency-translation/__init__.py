"""
Skill-Emergency-Translation Skill Package.
"""

from .skill import EmergencyTranslationSkill

def create_skill():
    return EmergencyTranslationSkill()

__all__ = ["EmergencyTranslationSkill", "create_skill"]
