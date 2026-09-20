"""
Skill-Smartthings Skill Package.
"""

from .skill import SmartthingsSkill

def create_skill():
    return SmartthingsSkill()

__all__ = ["SmartthingsSkill", "create_skill"]
