"""
Skill-Weather Skill Package.
"""

from .skill import WeatherSkill

def create_skill():
    return WeatherSkill()

__all__ = ["WeatherSkill", "create_skill"]
