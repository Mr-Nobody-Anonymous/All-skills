"""
Skill-Evacuation Skill Package.
"""

from .skill import EvacuationSkill

def create_skill():
    return EvacuationSkill()

__all__ = ["EvacuationSkill", "create_skill"]
