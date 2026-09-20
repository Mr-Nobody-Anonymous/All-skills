"""
Skill-Tip-Calculator Skill Package.
"""

from .skill import TipCalculatorSkill

def create_skill():
    return TipCalculatorSkill()

__all__ = ["TipCalculatorSkill", "create_skill"]
