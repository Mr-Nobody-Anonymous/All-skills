"""
Skill-Medication-Reminder Skill Package.
"""

from .skill import MedicationReminderSkill

def create_skill():
    return MedicationReminderSkill()

__all__ = ["MedicationReminderSkill", "create_skill"]
