"""
Skill-Fuel-Tracker Skill Package.
"""

from .skill import FuelTrackerSkill

def create_skill():
    return FuelTrackerSkill()

__all__ = ["FuelTrackerSkill", "create_skill"]
