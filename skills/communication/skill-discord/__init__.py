"""
Skill-Discord Skill Package.
"""

from .skill import DiscordSkill

def create_skill():
    return DiscordSkill()

__all__ = ["DiscordSkill", "create_skill"]
