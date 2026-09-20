"""
Skill-Dalle Skill Package.
"""

from .skill import DalleSkill

def create_skill():
    return DalleSkill()

__all__ = ["DalleSkill", "create_skill"]
