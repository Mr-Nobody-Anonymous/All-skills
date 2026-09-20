"""
Skill-Ring Skill Package.
"""

from .skill import RingSkill

def create_skill():
    return RingSkill()

__all__ = ["RingSkill", "create_skill"]
