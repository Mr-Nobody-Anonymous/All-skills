"""
Skill-Stocks Skill Package.
"""

from .skill import StocksSkill

def create_skill():
    return StocksSkill()

__all__ = ["StocksSkill", "create_skill"]
