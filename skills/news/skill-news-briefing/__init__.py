"""
Skill-News-Briefing Skill Package.
"""

from .skill import NewsBriefingSkill

def create_skill():
    return NewsBriefingSkill()

__all__ = ["NewsBriefingSkill", "create_skill"]
