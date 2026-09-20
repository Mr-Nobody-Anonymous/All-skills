"""
Skill-Mad-Libs Skill Package.
"""

from .skill import MadLibsSkill

def create_skill():
    return MadLibsSkill()

__all__ = ["MadLibsSkill", "create_skill"]
