"""
Skill-Parking Skill Package.
"""

from .skill import ParkingSkill

def create_skill():
    return ParkingSkill()

__all__ = ["ParkingSkill", "create_skill"]
