"""
Skill-Mortgage-Calculator Skill Package.
"""

from .skill import MortgageCalculatorSkill

def create_skill():
    return MortgageCalculatorSkill()

__all__ = ["MortgageCalculatorSkill", "create_skill"]
