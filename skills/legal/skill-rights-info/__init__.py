"""
Skill-Rights-Info Skill Package.
"""

from .skill import RightsInfoSkill

def create_skill():
    return RightsInfoSkill()

__all__ = ["RightsInfoSkill", "create_skill"]
