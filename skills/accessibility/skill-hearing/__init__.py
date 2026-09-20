"""
Skill-Hearing Skill Package.
"""

from .skill import HearingSkill

def create_skill():
    return HearingSkill()

__all__ = ["HearingSkill", "create_skill"]
