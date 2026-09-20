"""
Skill-Power Skill Package.
"""

from .skill import PowerSkill

def create_skill():
    return PowerSkill()

__all__ = ["PowerSkill", "create_skill"]
