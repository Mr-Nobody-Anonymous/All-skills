"""
Skill-Deal-Finder Skill Package.
"""

from .skill import DealFinderSkill

def create_skill():
    return DealFinderSkill()

__all__ = ["DealFinderSkill", "create_skill"]
