"""
Skill-How-To Skill Package.
"""

from .skill import HowToSkill

def create_skill():
    return HowToSkill()

__all__ = ["HowToSkill", "create_skill"]
