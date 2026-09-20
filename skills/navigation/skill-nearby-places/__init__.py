"""
Skill-Nearby-Places Skill Package.
"""

from .skill import NearbyPlacesSkill

def create_skill():
    return NearbyPlacesSkill()

__all__ = ["NearbyPlacesSkill", "create_skill"]
