"""
Skill-Wink Skill Package.
"""

from .skill import WinkSkill

def create_skill():
    return WinkSkill()

__all__ = ["WinkSkill", "create_skill"]
