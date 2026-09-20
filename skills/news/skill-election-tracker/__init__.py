"""
Skill-Election-Tracker Skill Package.
"""

from .skill import ElectionTrackerSkill

def create_skill():
    return ElectionTrackerSkill()

__all__ = ["ElectionTrackerSkill", "create_skill"]
