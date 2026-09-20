"""
Skill-Iss-Tracker Skill Package.
"""

from .skill import IssTrackerSkill

def create_skill():
    return IssTrackerSkill()

__all__ = ["IssTrackerSkill", "create_skill"]
