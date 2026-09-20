"""
Skill-Periodic-Table Skill Package.
"""

from .skill import PeriodicTableSkill

def create_skill():
    return PeriodicTableSkill()

__all__ = ["PeriodicTableSkill", "create_skill"]
