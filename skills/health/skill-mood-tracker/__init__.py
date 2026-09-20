"""
Skill-Mood-Tracker Skill Package.
"""

from .skill import MoodTrackerSkill

def create_skill():
    return MoodTrackerSkill()

__all__ = ["MoodTrackerSkill", "create_skill"]
