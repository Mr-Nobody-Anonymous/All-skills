"""
Skill-Car-Finder Skill Package.
"""

from .skill import CarFinderSkill

def create_skill():
    return CarFinderSkill()

__all__ = ["CarFinderSkill", "create_skill"]
