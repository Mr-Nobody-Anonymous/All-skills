"""
Skill-Api-Tester Skill Package.
"""

from .skill import ApiTesterSkill

def create_skill():
    return ApiTesterSkill()

__all__ = ["ApiTesterSkill", "create_skill"]
