"""
Skill-Moon-Phase Skill Package.
"""

from .skill import MoonPhaseSkill

def create_skill():
    return MoonPhaseSkill()

__all__ = ["MoonPhaseSkill", "create_skill"]
