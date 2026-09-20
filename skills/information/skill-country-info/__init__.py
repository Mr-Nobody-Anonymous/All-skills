"""
Skill-Country-Info Skill Package.
"""

from .skill import CountryInfoSkill

def create_skill():
    return CountryInfoSkill()

__all__ = ["CountryInfoSkill", "create_skill"]
