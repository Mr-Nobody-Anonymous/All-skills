"""
Skill-Songwriting Skill Package.
"""

from .skill import SongwritingSkill

def create_skill():
    return SongwritingSkill()

__all__ = ["SongwritingSkill", "create_skill"]
