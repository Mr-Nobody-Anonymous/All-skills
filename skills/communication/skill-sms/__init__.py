"""
Skill-Sms Skill Package.
"""

from .skill import SmsSkill

def create_skill():
    return SmsSkill()

__all__ = ["SmsSkill", "create_skill"]
