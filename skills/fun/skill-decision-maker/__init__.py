"""
Skill-Decision-Maker Skill Package.
"""

from .skill import DecisionMakerSkill

def create_skill():
    return DecisionMakerSkill()

__all__ = ["DecisionMakerSkill", "create_skill"]
