"""
Skill-Gift-Ideas Skill Package.
"""

from .skill import GiftIdeasSkill

def create_skill():
    return GiftIdeasSkill()

__all__ = ["GiftIdeasSkill", "create_skill"]
