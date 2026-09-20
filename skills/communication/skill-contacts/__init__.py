"""
Skill-Contacts Skill Package.
"""

from .skill import ContactsSkill

def create_skill():
    return ContactsSkill()

__all__ = ["ContactsSkill", "create_skill"]
