"""
Skill-Kodi Skill Package.
"""

from .skill import KodiSkill

def create_skill():
    return KodiSkill()

__all__ = ["KodiSkill", "create_skill"]
