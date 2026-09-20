"""
Skill-Planting-Calendar Skill Package.
"""

from .skill import PlantingCalendarSkill

def create_skill():
    return PlantingCalendarSkill()

__all__ = ["PlantingCalendarSkill", "create_skill"]
