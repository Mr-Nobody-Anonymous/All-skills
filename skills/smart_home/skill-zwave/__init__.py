"""
Skill-Zwave Skill Package.
"""

from .skill import ZwaveSkill

def create_skill():
    return ZwaveSkill()

__all__ = ["ZwaveSkill", "create_skill"]
