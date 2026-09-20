"""
Skill-Lab-Tools Skill Package.
"""

from .skill import LabToolsSkill

def create_skill():
    return LabToolsSkill()

__all__ = ["LabToolsSkill", "create_skill"]
