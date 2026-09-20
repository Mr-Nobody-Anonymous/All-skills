"""
Skill-Science-News Skill Package.
"""

from .skill import ScienceNewsSkill

def create_skill():
    return ScienceNewsSkill()

__all__ = ["ScienceNewsSkill", "create_skill"]
