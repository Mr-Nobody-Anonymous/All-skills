"""
Skill-Commodities Skill Package.
"""

from .skill import CommoditiesSkill

def create_skill():
    return CommoditiesSkill()

__all__ = ["CommoditiesSkill", "create_skill"]
