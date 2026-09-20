"""
Skill-Ci-Cd Skill Package.
"""

from .skill import CiCdSkill

def create_skill():
    return CiCdSkill()

__all__ = ["CiCdSkill", "create_skill"]
