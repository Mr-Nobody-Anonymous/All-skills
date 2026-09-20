"""
Skill-Flight-Tracker Skill Package.
"""

from .skill import FlightTrackerSkill

def create_skill():
    return FlightTrackerSkill()

__all__ = ["FlightTrackerSkill", "create_skill"]
