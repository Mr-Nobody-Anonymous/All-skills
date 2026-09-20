"""
Skill-Apple-Health Skill Package.
"""

from .skill import AppleHealthSkill

def create_skill():
    return AppleHealthSkill()

__all__ = ["AppleHealthSkill", "create_skill"]
