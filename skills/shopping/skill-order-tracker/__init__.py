"""
Skill-Order-Tracker Skill Package.
"""

from .skill import OrderTrackerSkill

def create_skill():
    return OrderTrackerSkill()

__all__ = ["OrderTrackerSkill", "create_skill"]
