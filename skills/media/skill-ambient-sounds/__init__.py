"""
Skill-Ambient-Sounds Skill Package.
"""

from .skill import AmbientSoundsSkill

def create_skill():
    return AmbientSoundsSkill()

__all__ = ["AmbientSoundsSkill", "create_skill"]
