"""
Skill-Sunrise-Sunset Skill Package.
"""

from .skill import SunriseSunsetSkill

def create_skill():
    return SunriseSunsetSkill()

__all__ = ["SunriseSunsetSkill", "create_skill"]
