"""
Skill-Ai-Music Skill Package.
"""

from .skill import AiMusicSkill

def create_skill():
    return AiMusicSkill()

__all__ = ["AiMusicSkill", "create_skill"]
