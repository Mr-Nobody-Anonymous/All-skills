"""
Skill-Matter Skill Package.
"""

from .skill import MatterSkill

def create_skill():
    return MatterSkill()

__all__ = ["MatterSkill", "create_skill"]
