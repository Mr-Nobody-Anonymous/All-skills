"""
Skill-Road-Conditions Skill Package.
"""

from .skill import RoadConditionsSkill

def create_skill():
    return RoadConditionsSkill()

__all__ = ["RoadConditionsSkill", "create_skill"]
