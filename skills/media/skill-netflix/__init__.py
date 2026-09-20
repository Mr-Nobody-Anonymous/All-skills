"""
Skill-Netflix Skill Package.
"""

from .skill import NetflixSkill

def create_skill():
    return NetflixSkill()

__all__ = ["NetflixSkill", "create_skill"]
