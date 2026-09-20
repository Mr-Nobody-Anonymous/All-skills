"""
Skill-Facts Skill Package.
"""

from .skill import FactsSkill

def create_skill():
    return FactsSkill()

__all__ = ["FactsSkill", "create_skill"]
