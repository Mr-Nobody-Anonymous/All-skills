"""
Skill-Loan-Calculator Skill Package.
"""

from .skill import LoanCalculatorSkill

def create_skill():
    return LoanCalculatorSkill()

__all__ = ["LoanCalculatorSkill", "create_skill"]
