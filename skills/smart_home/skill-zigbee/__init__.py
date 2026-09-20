"""
Skill-Zigbee Skill Package.
"""

from .skill import ZigbeeSkill

def create_skill():
    return ZigbeeSkill()

__all__ = ["ZigbeeSkill", "create_skill"]
