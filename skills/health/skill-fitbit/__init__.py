"""
Skill-Fitbit Skill Package.
"""

from .skill import FitbitSkill

def create_skill():
    return FitbitSkill()

__all__ = ["FitbitSkill", "create_skill"]
