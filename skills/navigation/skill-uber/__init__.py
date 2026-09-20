"""
Skill-Uber Skill Package.
"""

from .skill import UberSkill

def create_skill():
    return UberSkill()

__all__ = ["UberSkill", "create_skill"]
