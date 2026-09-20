"""
Skill-Wyze Skill Package.
"""

from .skill import WyzeSkill

def create_skill():
    return WyzeSkill()

__all__ = ["WyzeSkill", "create_skill"]
