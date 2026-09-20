"""
Skill-Price-Comparison Skill Package.
"""

from .skill import PriceComparisonSkill

def create_skill():
    return PriceComparisonSkill()

__all__ = ["PriceComparisonSkill", "create_skill"]
