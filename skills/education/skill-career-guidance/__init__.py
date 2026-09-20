"""
Skill-Career-Guidance Skill Package.
"""

from .skill import CareerGuidanceSkill

def create_skill():
    return CareerGuidanceSkill()

__all__ = ["CareerGuidanceSkill", "create_skill"]
