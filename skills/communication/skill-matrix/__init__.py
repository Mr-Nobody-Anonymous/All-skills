"""
Skill-Matrix Skill Package.
"""

from .skill import MatrixSkill

def create_skill():
    return MatrixSkill()

__all__ = ["MatrixSkill", "create_skill"]
