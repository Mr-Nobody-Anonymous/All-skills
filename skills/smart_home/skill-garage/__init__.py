"""
Skill-Garage Skill Package.
"""

from .skill import GarageSkill

def create_skill():
    return GarageSkill()

__all__ = ["GarageSkill", "create_skill"]
