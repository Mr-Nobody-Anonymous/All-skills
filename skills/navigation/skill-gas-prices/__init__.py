"""
Skill-Gas-Prices Skill Package.
"""

from .skill import GasPricesSkill

def create_skill():
    return GasPricesSkill()

__all__ = ["GasPricesSkill", "create_skill"]
