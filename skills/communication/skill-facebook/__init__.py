"""
Skill-Facebook Skill Package.
"""

from .skill import FacebookSkill

def create_skill():
    return FacebookSkill()

__all__ = ["FacebookSkill", "create_skill"]
