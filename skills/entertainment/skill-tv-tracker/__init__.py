"""
Skill-Tv-Tracker Skill Package.
"""

from .skill import TvTrackerSkill

def create_skill():
    return TvTrackerSkill()

__all__ = ["TvTrackerSkill", "create_skill"]
