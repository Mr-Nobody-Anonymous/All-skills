"""
Skill-Instagram Skill Package.
"""

from .skill import InstagramSkill

def create_skill():
    return InstagramSkill()

__all__ = ["InstagramSkill", "create_skill"]
