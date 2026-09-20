"""
Skill-Maintenance Skill Package.
"""

from .skill import MaintenanceSkill

def create_skill():
    return MaintenanceSkill()

__all__ = ["MaintenanceSkill", "create_skill"]
