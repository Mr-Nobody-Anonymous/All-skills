"""
Skill-Financial-News Skill Package.
"""

from .skill import FinancialNewsSkill

def create_skill():
    return FinancialNewsSkill()

__all__ = ["FinancialNewsSkill", "create_skill"]
