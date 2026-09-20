"""
Skill-Survival Skill Package.
"""

from .skill import SurvivalSkill

def create_skill():
    return SurvivalSkill()

__all__ = ["SurvivalSkill", "create_skill"]
