"""
Skill-Internet-Radio Skill Package.
"""

from .skill import InternetRadioSkill

def create_skill():
    return InternetRadioSkill()

__all__ = ["InternetRadioSkill", "create_skill"]
