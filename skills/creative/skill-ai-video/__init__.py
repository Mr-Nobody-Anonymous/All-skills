"""
Skill-Ai-Video Skill Package.
"""

from .skill import AiVideoSkill

def create_skill():
    return AiVideoSkill()

__all__ = ["AiVideoSkill", "create_skill"]
