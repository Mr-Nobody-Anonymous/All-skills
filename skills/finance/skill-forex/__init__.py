"""
Skill-Forex Skill Package.
"""

from .skill import ForexSkill

def create_skill():
    return ForexSkill()

__all__ = ["ForexSkill", "create_skill"]
