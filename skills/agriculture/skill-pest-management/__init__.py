"""
Skill-Pest-Management Skill Package.
"""

from .skill import PestManagementSkill

def create_skill():
    return PestManagementSkill()

__all__ = ["PestManagementSkill", "create_skill"]
