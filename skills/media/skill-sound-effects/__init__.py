"""
Skill-Sound-Effects Skill Package.
"""

from .skill import SoundEffectsSkill

def create_skill():
    return SoundEffectsSkill()

__all__ = ["SoundEffectsSkill", "create_skill"]
