"""
Skill-Vehicle-Valuation Skill Package.
"""

from .skill import VehicleValuationSkill

def create_skill():
    return VehicleValuationSkill()

__all__ = ["VehicleValuationSkill", "create_skill"]
