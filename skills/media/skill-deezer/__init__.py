"""
Skill-Deezer Skill Package.
"""

from .skill import DeezerSkill

def create_skill():
    return DeezerSkill()

__all__ = ["DeezerSkill", "create_skill"]
