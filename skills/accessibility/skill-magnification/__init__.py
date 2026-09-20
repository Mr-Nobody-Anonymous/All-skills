"""
Skill-Magnification Skill Package.
"""

from .skill import MagnificationSkill

def create_skill():
    return MagnificationSkill()

__all__ = ["MagnificationSkill", "create_skill"]
