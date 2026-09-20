"""
Skill-Portfolio Skill Package.
"""

from .skill import PortfolioSkill

def create_skill():
    return PortfolioSkill()

__all__ = ["PortfolioSkill", "create_skill"]
