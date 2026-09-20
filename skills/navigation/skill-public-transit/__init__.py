"""
Skill-Public-Transit Skill Package.
"""

from .skill import PublicTransitSkill

def create_skill():
    return PublicTransitSkill()

__all__ = ["PublicTransitSkill", "create_skill"]
