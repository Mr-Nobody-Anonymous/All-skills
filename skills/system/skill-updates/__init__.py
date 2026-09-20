"""
Skill-Updates Skill Package.
"""

from .skill import UpdatesSkill

def create_skill():
    return UpdatesSkill()

__all__ = ["UpdatesSkill", "create_skill"]
