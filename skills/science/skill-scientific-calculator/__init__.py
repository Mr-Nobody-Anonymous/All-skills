"""
Skill-Scientific-Calculator Skill Package.
"""

from .skill import ScientificCalculatorSkill

def create_skill():
    return ScientificCalculatorSkill()

__all__ = ["ScientificCalculatorSkill", "create_skill"]
