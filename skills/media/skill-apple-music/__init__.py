"""
Skill-Apple-Music Skill Package.
"""

from .skill import AppleMusicSkill

def create_skill():
    return AppleMusicSkill()

__all__ = ["AppleMusicSkill", "create_skill"]
