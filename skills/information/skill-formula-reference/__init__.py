"""
Skill-Formula-Reference Skill Package.
"""

from .skill import FormulaReferenceSkill

def create_skill():
    return FormulaReferenceSkill()

__all__ = ["FormulaReferenceSkill", "create_skill"]
