"""
Skill-Store-Finder Skill Package.
"""

from .skill import StoreFinderSkill

def create_skill():
    return StoreFinderSkill()

__all__ = ["StoreFinderSkill", "create_skill"]
