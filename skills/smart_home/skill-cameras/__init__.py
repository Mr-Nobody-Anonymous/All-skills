"""
Skill-Cameras Skill Package.
"""

from .skill import CamerasSkill

def create_skill():
    return CamerasSkill()

__all__ = ["CamerasSkill", "create_skill"]
