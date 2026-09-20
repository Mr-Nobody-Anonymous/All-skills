"""
Skill-Tech-News Skill Package.
"""

from .skill import TechNewsSkill

def create_skill():
    return TechNewsSkill()

__all__ = ["TechNewsSkill", "create_skill"]
