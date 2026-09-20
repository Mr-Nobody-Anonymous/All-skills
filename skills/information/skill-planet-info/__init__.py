"""
Skill-Planet-Info Skill Package.
"""

from .skill import PlanetInfoSkill

def create_skill():
    return PlanetInfoSkill()

__all__ = ["PlanetInfoSkill", "create_skill"]
