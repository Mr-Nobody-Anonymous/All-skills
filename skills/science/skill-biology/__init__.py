"""
Skill-Biology Skill Package.
"""

from .skill import BiologySkill

def create_skill():
    return BiologySkill()

__all__ = ["BiologySkill", "create_skill"]
