"""
Skill-Gratitude Skill Package.
"""

from .skill import GratitudeSkill

def create_skill():
    return GratitudeSkill()

__all__ = ["GratitudeSkill", "create_skill"]
