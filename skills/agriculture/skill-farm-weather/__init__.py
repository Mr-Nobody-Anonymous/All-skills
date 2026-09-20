"""
Skill-Farm-Weather Skill Package.
"""

from .skill import FarmWeatherSkill

def create_skill():
    return FarmWeatherSkill()

__all__ = ["FarmWeatherSkill", "create_skill"]
