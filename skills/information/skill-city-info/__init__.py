"""
Skill-City-Info Skill Package.
"""

from .skill import CityInfoSkill

def create_skill():
    return CityInfoSkill()

__all__ = ["CityInfoSkill", "create_skill"]
