"""
Skill-Tesla Skill Package.
"""

from .skill import TeslaSkill

def create_skill():
    return TeslaSkill()

__all__ = ["TeslaSkill", "create_skill"]
