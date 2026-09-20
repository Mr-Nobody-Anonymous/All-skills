"""
Skill-Soundcloud Skill Package.
"""

from .skill import SoundcloudSkill

def create_skill():
    return SoundcloudSkill()

__all__ = ["SoundcloudSkill", "create_skill"]
