"""
Skill-Volunteer Skill Package.
"""

from .skill import VolunteerSkill

def create_skill():
    return VolunteerSkill()

__all__ = ["VolunteerSkill", "create_skill"]
