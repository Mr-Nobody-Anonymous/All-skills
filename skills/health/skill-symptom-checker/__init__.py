"""
Skill-Symptom-Checker Skill Package.
"""

from .skill import SymptomCheckerSkill

def create_skill():
    return SymptomCheckerSkill()

__all__ = ["SymptomCheckerSkill", "create_skill"]
