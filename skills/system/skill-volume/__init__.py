"""
Skill-Volume Skill Package.
"""

from .skill import VolumeSkill

def create_skill():
    return VolumeSkill()

__all__ = ["VolumeSkill", "create_skill"]
