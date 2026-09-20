"""
Skill-Wildfire Skill Package.
"""

from .skill import WildfireSkill

def create_skill():
    return WildfireSkill()

__all__ = ["WildfireSkill", "create_skill"]
