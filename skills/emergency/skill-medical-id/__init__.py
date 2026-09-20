"""
Skill-Medical-Id Skill Package.
"""

from .skill import MedicalIdSkill

def create_skill():
    return MedicalIdSkill()

__all__ = ["MedicalIdSkill", "create_skill"]
