"""
Skill-Emby Skill Package.
"""

from .skill import EmbySkill

def create_skill():
    return EmbySkill()

__all__ = ["EmbySkill", "create_skill"]
