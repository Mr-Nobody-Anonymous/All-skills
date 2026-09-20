"""
Skill-Tax-Calculator Skill Package.
"""

from .skill import TaxCalculatorSkill

def create_skill():
    return TaxCalculatorSkill()

__all__ = ["TaxCalculatorSkill", "create_skill"]
