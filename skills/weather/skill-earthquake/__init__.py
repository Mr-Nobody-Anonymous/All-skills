"""
Skill-Earthquake Skill Package.
"""

from .skill import EarthquakeSkill

def create_skill():
    return EarthquakeSkill()

__all__ = ["EarthquakeSkill", "create_skill"]
