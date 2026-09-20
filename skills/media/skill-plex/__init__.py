"""
Skill-Plex Skill Package.
"""

from .skill import PlexSkill

def create_skill():
    return PlexSkill()

__all__ = ["PlexSkill", "create_skill"]
