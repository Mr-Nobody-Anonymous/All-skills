"""
Skill-Ecobee Skill Package.
"""

from .skill import EcobeeSkill

def create_skill():
    return EcobeeSkill()

__all__ = ["EcobeeSkill", "create_skill"]
