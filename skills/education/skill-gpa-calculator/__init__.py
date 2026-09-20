"""
Skill-Gpa-Calculator Skill Package.
"""

from .skill import GpaCalculatorSkill

def create_skill():
    return GpaCalculatorSkill()

__all__ = ["GpaCalculatorSkill", "create_skill"]
