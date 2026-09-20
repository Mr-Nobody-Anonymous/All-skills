"""
Skill-Timezone Skill Package.
"""

from .skill import TimezoneSkill

def create_skill():
    return TimezoneSkill()

__all__ = ["TimezoneSkill", "create_skill"]
