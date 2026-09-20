"""
Skill-Fortune-Cookie Skill Package.
"""

from .skill import FortuneCookieSkill

def create_skill():
    return FortuneCookieSkill()

__all__ = ["FortuneCookieSkill", "create_skill"]
