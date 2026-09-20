"""
Skill-Legal-Definitions Skill Package.
"""

from .skill import LegalDefinitionsSkill

def create_skill():
    return LegalDefinitionsSkill()

__all__ = ["LegalDefinitionsSkill", "create_skill"]
