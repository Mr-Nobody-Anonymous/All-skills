"""
Skill-Youtube-Music Skill Package.
"""

from .skill import YoutubeMusicSkill

def create_skill():
    return YoutubeMusicSkill()

__all__ = ["YoutubeMusicSkill", "create_skill"]
