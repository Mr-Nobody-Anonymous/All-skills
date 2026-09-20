"""
Skill-Retirement-Calculator Skill Package.
"""

from .skill import RetirementCalculatorSkill

def create_skill():
    return RetirementCalculatorSkill()

__all__ = ["RetirementCalculatorSkill", "create_skill"]
