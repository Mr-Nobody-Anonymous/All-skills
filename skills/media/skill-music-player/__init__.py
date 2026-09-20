"""
Skill-Music-Player Skill Package.
"""

from .skill import MusicPlayerSkill

def create_skill():
    return MusicPlayerSkill()

__all__ = ["MusicPlayerSkill", "create_skill"]
