"""
Skill-Playlist Skill Package.
"""

from .skill import PlaylistSkill

def create_skill():
    return PlaylistSkill()

__all__ = ["PlaylistSkill", "create_skill"]
