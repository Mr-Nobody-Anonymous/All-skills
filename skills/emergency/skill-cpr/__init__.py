"""
Skill-Cpr Skill Package.
"""

from .skill import CprSkill

def create_skill():
    return CprSkill()

__all__ = ["CprSkill", "create_skill"]
