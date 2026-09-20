"""
Skill-Sonos Skill Package.
"""

from .skill import SonosSkill

def create_skill():
    return SonosSkill()

__all__ = ["SonosSkill", "create_skill"]
