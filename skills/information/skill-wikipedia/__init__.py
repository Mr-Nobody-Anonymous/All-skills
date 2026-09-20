"""
Skill-Wikipedia Skill Package.
"""

from .skill import WikipediaSkill

def create_skill():
    return WikipediaSkill()

__all__ = ["WikipediaSkill", "create_skill"]
