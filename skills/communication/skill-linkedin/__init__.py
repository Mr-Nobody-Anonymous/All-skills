"""
Skill-Linkedin Skill Package.
"""

from .skill import LinkedinSkill

def create_skill():
    return LinkedinSkill()

__all__ = ["LinkedinSkill", "create_skill"]
