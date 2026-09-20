"""
Skill-Reddit Skill Package.
"""

from .skill import RedditSkill

def create_skill():
    return RedditSkill()

__all__ = ["RedditSkill", "create_skill"]
