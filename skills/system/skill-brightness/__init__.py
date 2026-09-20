"""
Skill-Brightness Skill Package.
"""

from .skill import BrightnessSkill

def create_skill():
    return BrightnessSkill()

__all__ = ["BrightnessSkill", "create_skill"]
