"""
Skill-Video-Call Skill Package.
"""

from .skill import VideoCallSkill

def create_skill():
    return VideoCallSkill()

__all__ = ["VideoCallSkill", "create_skill"]
