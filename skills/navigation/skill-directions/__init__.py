"""
Skill-Directions Skill Package.
"""

from .skill import DirectionsSkill

def create_skill():
    return DirectionsSkill()

__all__ = ["DirectionsSkill", "create_skill"]
