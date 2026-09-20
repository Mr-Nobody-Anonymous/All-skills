"""
Skill-Date-Ideas Skill Package.
"""

from .skill import DateIdeasSkill

def create_skill():
    return DateIdeasSkill()

__all__ = ["DateIdeasSkill", "create_skill"]
