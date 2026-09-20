"""
Skill-Scenes Skill Package.
"""

from .skill import ScenesSkill

def create_skill():
    return ScenesSkill()

__all__ = ["ScenesSkill", "create_skill"]
