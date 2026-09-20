"""
Skill-Home-Assistant Skill Package.
"""

from .skill import HomeAssistantSkill

def create_skill():
    return HomeAssistantSkill()

__all__ = ["HomeAssistantSkill", "create_skill"]
