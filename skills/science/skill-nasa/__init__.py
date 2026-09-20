"""
Skill-Nasa Skill Package.
"""

from .skill import NasaSkill

def create_skill():
    return NasaSkill()

__all__ = ["NasaSkill", "create_skill"]
