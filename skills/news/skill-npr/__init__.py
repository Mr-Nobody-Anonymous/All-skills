"""
Skill-Npr Skill Package.
"""

from .skill import NprSkill

def create_skill():
    return NprSkill()

__all__ = ["NprSkill", "create_skill"]
