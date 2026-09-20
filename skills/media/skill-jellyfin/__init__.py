"""
Skill-Jellyfin Skill Package.
"""

from .skill import JellyfinSkill

def create_skill():
    return JellyfinSkill()

__all__ = ["JellyfinSkill", "create_skill"]
