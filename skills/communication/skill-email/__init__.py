"""
Skill-Email Skill Package.
"""

from .skill import EmailSkill

def create_skill():
    return EmailSkill()

__all__ = ["EmailSkill", "create_skill"]
