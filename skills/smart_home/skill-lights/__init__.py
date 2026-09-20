"""
Skill-Lights Skill Package.
"""

from .skill import LightsSkill

def create_skill():
    return LightsSkill()

__all__ = ["LightsSkill", "create_skill"]
