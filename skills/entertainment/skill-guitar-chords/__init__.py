"""
Skill-Guitar-Chords Skill Package.
"""

from .skill import GuitarChordsSkill

def create_skill():
    return GuitarChordsSkill()

__all__ = ["GuitarChordsSkill", "create_skill"]
