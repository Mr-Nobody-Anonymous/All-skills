"""
Skill-Carbon-Footprint Skill Package.
"""

from .skill import CarbonFootprintSkill

def create_skill():
    return CarbonFootprintSkill()

__all__ = ["CarbonFootprintSkill", "create_skill"]
