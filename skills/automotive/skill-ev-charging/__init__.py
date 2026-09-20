"""
Skill-Ev-Charging Skill Package.
"""

from .skill import EvChargingSkill

def create_skill():
    return EvChargingSkill()

__all__ = ["EvChargingSkill", "create_skill"]
