"""
Skill-Node-Red Skill Package.
"""

from .skill import NodeRedSkill

def create_skill():
    return NodeRedSkill()

__all__ = ["NodeRedSkill", "create_skill"]
