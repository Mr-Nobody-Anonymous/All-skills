"""
Skill-Severe-Weather Skill Package.
"""

from .skill import SevereWeatherSkill

def create_skill():
    return SevereWeatherSkill()

__all__ = ["SevereWeatherSkill", "create_skill"]
