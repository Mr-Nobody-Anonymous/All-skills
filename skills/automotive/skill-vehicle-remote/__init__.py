"""
Skill-Vehicle-Remote Skill Package.
"""

from .skill import VehicleRemoteSkill

def create_skill():
    return VehicleRemoteSkill()

__all__ = ["VehicleRemoteSkill", "create_skill"]
