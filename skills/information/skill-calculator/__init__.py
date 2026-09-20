"""
Skill-Calculator Skill Package.
"""

from .skill import CalculatorSkill

def create_skill():
    return CalculatorSkill()

__all__ = ["CalculatorSkill", "create_skill"]
