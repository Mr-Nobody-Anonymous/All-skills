"""
Skill-News Skill Package.
"""

from .skill import NewsSkill

def create_skill():
    return NewsSkill()

__all__ = ["NewsSkill", "create_skill"]
