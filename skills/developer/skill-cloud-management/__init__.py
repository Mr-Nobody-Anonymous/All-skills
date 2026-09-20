"""
Skill-Cloud-Management Skill Package.
"""

from .skill import CloudManagementSkill

def create_skill():
    return CloudManagementSkill()

__all__ = ["CloudManagementSkill", "create_skill"]
