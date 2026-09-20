"""
Skill-Proverbs Skill Package.
"""

from .skill import ProverbsSkill

def create_skill():
    return ProverbsSkill()

__all__ = ["ProverbsSkill", "create_skill"]
