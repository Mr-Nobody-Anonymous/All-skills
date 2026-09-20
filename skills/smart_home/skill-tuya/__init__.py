"""
Skill-Tuya Skill Package.
"""

from .skill import TuyaSkill

def create_skill():
    return TuyaSkill()

__all__ = ["TuyaSkill", "create_skill"]
