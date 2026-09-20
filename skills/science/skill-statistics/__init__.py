"""
Skill-Statistics Skill Package.
"""

from .skill import StatisticsSkill

def create_skill():
    return StatisticsSkill()

__all__ = ["StatisticsSkill", "create_skill"]
