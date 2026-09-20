"""
Skill-Dashcam Skill Package.
"""

from .skill import DashcamSkill

def create_skill():
    return DashcamSkill()

__all__ = ["DashcamSkill", "create_skill"]
