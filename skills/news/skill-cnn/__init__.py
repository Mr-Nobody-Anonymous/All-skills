"""
Skill-Cnn Skill Package.
"""

from .skill import CnnSkill

def create_skill():
    return CnnSkill()

__all__ = ["CnnSkill", "create_skill"]
