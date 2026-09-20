"""
Skill-Reuters Skill Package.
"""

from .skill import ReutersSkill

def create_skill():
    return ReutersSkill()

__all__ = ["ReutersSkill", "create_skill"]
