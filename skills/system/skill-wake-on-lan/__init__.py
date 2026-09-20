"""
Skill-Wake-On-Lan Skill Package.
"""

from .skill import WakeOnLanSkill

def create_skill():
    return WakeOnLanSkill()

__all__ = ["WakeOnLanSkill", "create_skill"]
