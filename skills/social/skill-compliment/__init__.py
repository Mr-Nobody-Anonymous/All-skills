"""
Skill-Compliment Skill Package.
"""

from .skill import ComplimentSkill

def create_skill():
    return ComplimentSkill()

__all__ = ["ComplimentSkill", "create_skill"]
