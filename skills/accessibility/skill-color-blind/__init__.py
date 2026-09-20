"""
Skill-Color-Blind Skill Package.
"""

from .skill import ColorBlindSkill

def create_skill():
    return ColorBlindSkill()

__all__ = ["ColorBlindSkill", "create_skill"]
