"""
Skill-Stories Skill Package.
"""

from .skill import StoriesSkill

def create_skill():
    return StoriesSkill()

__all__ = ["StoriesSkill", "create_skill"]
