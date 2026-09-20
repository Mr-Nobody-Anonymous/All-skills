"""
Skill-Mental-Health Skill Package.
"""

from .skill import MentalHealthSkill

def create_skill():
    return MentalHealthSkill()

__all__ = ["MentalHealthSkill", "create_skill"]
