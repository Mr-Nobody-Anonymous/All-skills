"""
Skill-Phone-Call Skill Package.
"""

from .skill import PhoneCallSkill

def create_skill():
    return PhoneCallSkill()

__all__ = ["PhoneCallSkill", "create_skill"]
