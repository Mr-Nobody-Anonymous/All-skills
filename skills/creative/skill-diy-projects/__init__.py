"""
Skill-Diy-Projects Skill Package.
"""

from .skill import DiyProjectsSkill

def create_skill():
    return DiyProjectsSkill()

__all__ = ["DiyProjectsSkill", "create_skill"]
