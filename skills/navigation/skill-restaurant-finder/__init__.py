"""
Skill-Restaurant-Finder Skill Package.
"""

from .skill import RestaurantFinderSkill

def create_skill():
    return RestaurantFinderSkill()

__all__ = ["RestaurantFinderSkill", "create_skill"]
