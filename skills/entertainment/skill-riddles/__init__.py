"""
Skill-Riddles Skill Package.
"""

from .skill import RiddlesSkill

def create_skill():
    return RiddlesSkill()

__all__ = ["RiddlesSkill", "create_skill"]
