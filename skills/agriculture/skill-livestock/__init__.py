"""
Skill-Livestock Skill Package.
"""

from .skill import LivestockSkill

def create_skill():
    return LivestockSkill()

__all__ = ["LivestockSkill", "create_skill"]
