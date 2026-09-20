"""
Skill-Metronome Skill Package.
"""

from .skill import MetronomeSkill

def create_skill():
    return MetronomeSkill()

__all__ = ["MetronomeSkill", "create_skill"]
