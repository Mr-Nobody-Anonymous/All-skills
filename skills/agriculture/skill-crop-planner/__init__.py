"""
Skill-Crop-Planner Skill Package.
"""

from .skill import CropPlannerSkill

def create_skill():
    return CropPlannerSkill()

__all__ = ["CropPlannerSkill", "create_skill"]
