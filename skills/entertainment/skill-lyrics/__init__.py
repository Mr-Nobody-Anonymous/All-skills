"""
Skill-Lyrics Skill Package.
"""

from .skill import LyricsSkill

def create_skill():
    return LyricsSkill()

__all__ = ["LyricsSkill", "create_skill"]
