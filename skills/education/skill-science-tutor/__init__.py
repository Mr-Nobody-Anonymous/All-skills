"""
Skill-Science-Tutor Skill Package.
"""

from .skill import ScienceTutorSkill

def create_skill():
    return ScienceTutorSkill()

__all__ = ["ScienceTutorSkill", "create_skill"]
