"""
Skill-Emergency-Call Skill Package.
"""

from .skill import EmergencyCallSkill

def create_skill():
    return EmergencyCallSkill()

__all__ = ["EmergencyCallSkill", "create_skill"]
