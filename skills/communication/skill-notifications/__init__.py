"""
Skill-Notifications Skill Package.
"""

from .skill import NotificationsSkill

def create_skill():
    return NotificationsSkill()

__all__ = ["NotificationsSkill", "create_skill"]
