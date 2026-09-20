"""
Skill-Domoticz Skill Package.
"""

from .skill import DomoticzSkill

def create_skill():
    return DomoticzSkill()

__all__ = ["DomoticzSkill", "create_skill"]
