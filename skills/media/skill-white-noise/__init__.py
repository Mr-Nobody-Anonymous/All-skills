"""
Skill-White-Noise Skill Package.
"""

from .skill import WhiteNoiseSkill

def create_skill():
    return WhiteNoiseSkill()

__all__ = ["WhiteNoiseSkill", "create_skill"]
