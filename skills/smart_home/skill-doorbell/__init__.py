"""
Skill-Doorbell Skill Package.
"""

from .skill import DoorbellSkill

def create_skill():
    return DoorbellSkill()

__all__ = ["DoorbellSkill", "create_skill"]
