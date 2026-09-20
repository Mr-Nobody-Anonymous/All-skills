"""
Skill-First-Aid Skill Package.
"""

from .skill import FirstAidSkill

def create_skill():
    return FirstAidSkill()

__all__ = ["FirstAidSkill", "create_skill"]
