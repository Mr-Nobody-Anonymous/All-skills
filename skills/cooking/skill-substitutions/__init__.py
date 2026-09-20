"""
Skill-Substitutions Skill Package.
"""

from .skill import SubstitutionsSkill

def create_skill():
    return SubstitutionsSkill()

__all__ = ["SubstitutionsSkill", "create_skill"]
