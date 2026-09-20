"""
Skill-Space-Launches Skill Package.
"""

from .skill import SpaceLaunchesSkill

def create_skill():
    return SpaceLaunchesSkill()

__all__ = ["SpaceLaunchesSkill", "create_skill"]
