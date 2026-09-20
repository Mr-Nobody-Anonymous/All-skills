"""
Skill-Geography-Quiz Skill Package.
"""

from .skill import GeographyQuizSkill

def create_skill():
    return GeographyQuizSkill()

__all__ = ["GeographyQuizSkill", "create_skill"]
