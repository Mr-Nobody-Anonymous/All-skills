"""
Skill-Arlo Skill Package.
"""

from .skill import ArloSkill

def create_skill():
    return ArloSkill()

__all__ = ["ArloSkill", "create_skill"]
