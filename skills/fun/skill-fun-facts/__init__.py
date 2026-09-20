"""
Skill-Fun-Facts Skill Package.
"""

from .skill import FunFactsSkill

def create_skill():
    return FunFactsSkill()

__all__ = ["FunFactsSkill", "create_skill"]
