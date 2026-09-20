"""
Skill-Settings Skill Package.
"""

from .skill import SettingsSkill

def create_skill():
    return SettingsSkill()

__all__ = ["SettingsSkill", "create_skill"]
