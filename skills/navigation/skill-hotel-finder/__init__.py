"""
Skill-Hotel-Finder Skill Package.
"""

from .skill import HotelFinderSkill

def create_skill():
    return HotelFinderSkill()

__all__ = ["HotelFinderSkill", "create_skill"]
