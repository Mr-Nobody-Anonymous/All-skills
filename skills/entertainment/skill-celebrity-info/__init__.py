"""
Skill-Celebrity-Info Skill Package.
"""

from .skill import CelebrityInfoSkill

def create_skill():
    return CelebrityInfoSkill()

__all__ = ["CelebrityInfoSkill", "create_skill"]
