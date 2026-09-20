"""
Skill-Astronomy-Events Skill Package.
"""

from .skill import AstronomyEventsSkill

def create_skill():
    return AstronomyEventsSkill()

__all__ = ["AstronomyEventsSkill", "create_skill"]
