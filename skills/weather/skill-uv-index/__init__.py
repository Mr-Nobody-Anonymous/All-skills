"""
Skill-Uv-Index Skill Package.
"""

from .skill import UvIndexSkill

def create_skill():
    return UvIndexSkill()

__all__ = ["UvIndexSkill", "create_skill"]
