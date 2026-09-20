"""
Skill-Would-You-Rather Skill Package.
"""

from .skill import WouldYouRatherSkill

def create_skill():
    return WouldYouRatherSkill()

__all__ = ["WouldYouRatherSkill", "create_skill"]
