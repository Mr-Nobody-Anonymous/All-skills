"""
Skill-Charity Skill Package.
"""

from .skill import CharitySkill

def create_skill():
    return CharitySkill()

__all__ = ["CharitySkill", "create_skill"]
