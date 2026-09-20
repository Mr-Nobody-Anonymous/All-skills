"""
Skill-Personality-Test Skill Package.
"""

from .skill import PersonalityTestSkill

def create_skill():
    return PersonalityTestSkill()

__all__ = ["PersonalityTestSkill", "create_skill"]
