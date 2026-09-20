"""
Skill-Apps Skill Package.
"""

from .skill import AppsSkill

def create_skill():
    return AppsSkill()

__all__ = ["AppsSkill", "create_skill"]
