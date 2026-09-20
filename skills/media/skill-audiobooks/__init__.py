"""
Skill-Audiobooks Skill Package.
"""

from .skill import AudiobooksSkill

def create_skill():
    return AudiobooksSkill()

__all__ = ["AudiobooksSkill", "create_skill"]
