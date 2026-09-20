"""
Skill-Affirmation Skill Package.
"""

from .skill import AffirmationSkill

def create_skill():
    return AffirmationSkill()

__all__ = ["AffirmationSkill", "create_skill"]
