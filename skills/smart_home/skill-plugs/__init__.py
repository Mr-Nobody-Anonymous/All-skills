"""
Skill-Plugs Skill Package.
"""

from .skill import PlugsSkill

def create_skill():
    return PlugsSkill()

__all__ = ["PlugsSkill", "create_skill"]
