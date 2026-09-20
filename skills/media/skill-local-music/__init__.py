"""
Skill-Local-Music Skill Package.
"""

from .skill import LocalMusicSkill

def create_skill():
    return LocalMusicSkill()

__all__ = ["LocalMusicSkill", "create_skill"]
