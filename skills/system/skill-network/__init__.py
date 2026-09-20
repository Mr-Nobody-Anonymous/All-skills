"""
Skill-Network Skill Package.
"""

from .skill import NetworkSkill

def create_skill():
    return NetworkSkill()

__all__ = ["NetworkSkill", "create_skill"]
