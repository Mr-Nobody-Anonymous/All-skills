"""
Skill-Twitter Skill Package.
"""

from .skill import TwitterSkill

def create_skill():
    return TwitterSkill()

__all__ = ["TwitterSkill", "create_skill"]
