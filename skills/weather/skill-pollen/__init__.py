"""
Skill-Pollen Skill Package.
"""

from .skill import PollenSkill

def create_skill():
    return PollenSkill()

__all__ = ["PollenSkill", "create_skill"]
