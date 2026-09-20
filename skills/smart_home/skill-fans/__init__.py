"""
Skill-Fans Skill Package.
"""

from .skill import FansSkill

def create_skill():
    return FansSkill()

__all__ = ["FansSkill", "create_skill"]
