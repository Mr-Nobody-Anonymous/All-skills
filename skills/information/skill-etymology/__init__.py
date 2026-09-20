"""
Skill-Etymology Skill Package.
"""

from .skill import EtymologySkill

def create_skill():
    return EtymologySkill()

__all__ = ["EtymologySkill", "create_skill"]
