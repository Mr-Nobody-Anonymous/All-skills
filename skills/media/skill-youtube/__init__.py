"""
Skill-Youtube Skill Package.
"""

from .skill import YoutubeSkill

def create_skill():
    return YoutubeSkill()

__all__ = ["YoutubeSkill", "create_skill"]
