"""
Skill-Telegram Skill Package.
"""

from .skill import TelegramSkill

def create_skill():
    return TelegramSkill()

__all__ = ["TelegramSkill", "create_skill"]
