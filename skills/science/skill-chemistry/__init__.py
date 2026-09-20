"""
Skill-Chemistry Skill Package.
"""

from .skill import ChemistrySkill

def create_skill():
    return ChemistrySkill()

__all__ = ["ChemistrySkill", "create_skill"]
