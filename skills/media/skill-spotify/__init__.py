"""
Skill-Spotify Skill Package.
"""

from .skill import SpotifySkill

def create_skill():
    return SpotifySkill()

__all__ = ["SpotifySkill", "create_skill"]
