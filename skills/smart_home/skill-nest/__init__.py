"""
Skill-Nest Skill Package.
"""

from .skill import NestSkill

def create_skill():
    return NestSkill()

__all__ = ["NestSkill", "create_skill"]
