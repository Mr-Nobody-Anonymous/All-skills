"""
Skill-Routines Skill Package.
"""

from .skill import RoutinesSkill

def create_skill():
    return RoutinesSkill()

__all__ = ["RoutinesSkill", "create_skill"]
