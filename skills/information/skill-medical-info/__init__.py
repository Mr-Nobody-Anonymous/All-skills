"""
Skill-Medical-Info Skill Package.
"""

from .skill import MedicalInfoSkill

def create_skill():
    return MedicalInfoSkill()

__all__ = ["MedicalInfoSkill", "create_skill"]
