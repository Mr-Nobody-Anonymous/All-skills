"""
Skill-Animal-Info Skill Package.
"""

from .skill import AnimalInfoSkill

def create_skill():
    return AnimalInfoSkill()

__all__ = ["AnimalInfoSkill", "create_skill"]
