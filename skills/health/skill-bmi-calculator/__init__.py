"""
Skill-Bmi-Calculator Skill Package.
"""

from .skill import BmiCalculatorSkill

def create_skill():
    return BmiCalculatorSkill()

__all__ = ["BmiCalculatorSkill", "create_skill"]
