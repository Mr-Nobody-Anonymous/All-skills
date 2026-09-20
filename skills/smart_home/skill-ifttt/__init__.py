"""
Skill-Ifttt Skill Package.
"""

from .skill import IftttSkill

def create_skill():
    return IftttSkill()

__all__ = ["IftttSkill", "create_skill"]
