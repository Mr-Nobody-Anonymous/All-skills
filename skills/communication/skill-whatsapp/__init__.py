"""
Skill-Whatsapp Skill Package.
"""

from .skill import WhatsappSkill

def create_skill():
    return WhatsappSkill()

__all__ = ["WhatsappSkill", "create_skill"]
