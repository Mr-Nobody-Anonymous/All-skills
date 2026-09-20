"""
Skill-Price-Lookup Skill Package.
"""

from .skill import PriceLookupSkill

def create_skill():
    return PriceLookupSkill()

__all__ = ["PriceLookupSkill", "create_skill"]
