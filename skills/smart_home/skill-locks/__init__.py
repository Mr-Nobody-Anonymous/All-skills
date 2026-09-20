"""
Skill-Locks Skill Package.
"""

from .skill import LocksSkill

def create_skill():
    return LocksSkill()

__all__ = ["LocksSkill", "create_skill"]
