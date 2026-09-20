"""
Skill-Disaster-Prep Skill Package.
"""

from .skill import DisasterPrepSkill

def create_skill():
    return DisasterPrepSkill()

__all__ = ["DisasterPrepSkill", "create_skill"]
