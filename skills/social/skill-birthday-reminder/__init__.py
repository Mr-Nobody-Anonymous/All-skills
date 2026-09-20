"""
Skill-Birthday-Reminder Skill Package.
"""

from .skill import BirthdayReminderSkill

def create_skill():
    return BirthdayReminderSkill()

__all__ = ["BirthdayReminderSkill", "create_skill"]
