"""
Skill-Meditation Skill Package.
"""

from .skill import MeditationSkill

def create_skill():
    return MeditationSkill()

__all__ = ["MeditationSkill", "create_skill"]
