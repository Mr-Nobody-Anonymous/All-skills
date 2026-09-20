"""
Skill-Travel-Info Skill Package.
"""

from .skill import TravelInfoSkill

def create_skill():
    return TravelInfoSkill()

__all__ = ["TravelInfoSkill", "create_skill"]
