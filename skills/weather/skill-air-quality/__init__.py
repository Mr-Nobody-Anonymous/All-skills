"""
Skill-Air-Quality Skill Package.
"""

from .skill import AirQualitySkill

def create_skill():
    return AirQualitySkill()

__all__ = ["AirQualitySkill", "create_skill"]
