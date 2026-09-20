"""
Skill-Emergency-Contacts Skill Package.
"""

from .skill import EmergencyContactsSkill

def create_skill():
    return EmergencyContactsSkill()

__all__ = ["EmergencyContactsSkill", "create_skill"]
