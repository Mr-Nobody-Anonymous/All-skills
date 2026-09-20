"""
Skill-Physics Skill Package.
"""

from .skill import PhysicsSkill

def create_skill():
    return PhysicsSkill()

__all__ = ["PhysicsSkill", "create_skill"]
