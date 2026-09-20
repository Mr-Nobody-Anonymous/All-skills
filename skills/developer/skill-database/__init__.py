"""
Skill-Database Skill Package.
"""

from .skill import DatabaseSkill

def create_skill():
    return DatabaseSkill()

__all__ = ["DatabaseSkill", "create_skill"]
