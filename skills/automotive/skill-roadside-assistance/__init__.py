"""
Skill-Roadside-Assistance Skill Package.
"""

from .skill import RoadsideAssistanceSkill

def create_skill():
    return RoadsideAssistanceSkill()

__all__ = ["RoadsideAssistanceSkill", "create_skill"]
