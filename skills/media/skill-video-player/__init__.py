"""
Skill-Video-Player Skill Package.
"""

from .skill import VideoPlayerSkill

def create_skill():
    return VideoPlayerSkill()

__all__ = ["VideoPlayerSkill", "create_skill"]
