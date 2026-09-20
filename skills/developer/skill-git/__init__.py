"""
Skill-Git Skill Package.
"""

from .skill import GitSkill

def create_skill():
    return GitSkill()

__all__ = ["GitSkill", "create_skill"]
