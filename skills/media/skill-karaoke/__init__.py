"""
Skill-Karaoke Skill Package.
"""

from .skill import KaraokeSkill

def create_skill():
    return KaraokeSkill()

__all__ = ["KaraokeSkill", "create_skill"]
