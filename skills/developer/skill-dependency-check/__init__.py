"""
Skill-Dependency-Check Skill Package.
"""

from .skill import DependencyCheckSkill

def create_skill():
    return DependencyCheckSkill()

__all__ = ["DependencyCheckSkill", "create_skill"]
