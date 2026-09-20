"""
Skill-Soil-Info Skill Package.
"""

from .skill import SoilInfoSkill

def create_skill():
    return SoilInfoSkill()

__all__ = ["SoilInfoSkill", "create_skill"]
