"""
Skill-Plant-Info Skill Package.
"""

from .skill import PlantInfoSkill

def create_skill():
    return PlantInfoSkill()

__all__ = ["PlantInfoSkill", "create_skill"]
