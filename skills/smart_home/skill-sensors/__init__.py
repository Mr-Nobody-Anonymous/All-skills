"""
Skill-Sensors Skill Package.
"""

from .skill import SensorsSkill

def create_skill():
    return SensorsSkill()

__all__ = ["SensorsSkill", "create_skill"]
