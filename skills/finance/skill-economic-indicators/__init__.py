"""
Skill-Economic-Indicators Skill Package.
"""

from .skill import EconomicIndicatorsSkill

def create_skill():
    return EconomicIndicatorsSkill()

__all__ = ["EconomicIndicatorsSkill", "create_skill"]
