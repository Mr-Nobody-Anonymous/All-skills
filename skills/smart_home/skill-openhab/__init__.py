"""
Skill-Openhab Skill Package.
"""

from .skill import OpenhabSkill

def create_skill():
    return OpenhabSkill()

__all__ = ["OpenhabSkill", "create_skill"]
