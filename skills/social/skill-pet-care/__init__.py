"""
Skill-Pet-Care Skill Package.
"""

from .skill import PetCareSkill

def create_skill():
    return PetCareSkill()

__all__ = ["PetCareSkill", "create_skill"]
