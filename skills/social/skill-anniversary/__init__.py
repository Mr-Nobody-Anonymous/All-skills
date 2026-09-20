"""
Skill-Anniversary Skill Package.
"""

from .skill import AnniversarySkill

def create_skill():
    return AnniversarySkill()

__all__ = ["AnniversarySkill", "create_skill"]
