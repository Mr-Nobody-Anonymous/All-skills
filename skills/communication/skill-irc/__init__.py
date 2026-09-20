"""
Skill-Irc Skill Package.
"""

from .skill import IrcSkill

def create_skill():
    return IrcSkill()

__all__ = ["IrcSkill", "create_skill"]
