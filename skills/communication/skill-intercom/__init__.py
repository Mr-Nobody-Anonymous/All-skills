"""
Skill-Intercom Skill Package.
"""

from .skill import IntercomSkill

def create_skill():
    return IntercomSkill()

__all__ = ["IntercomSkill", "create_skill"]
