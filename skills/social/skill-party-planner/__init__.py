"""
Skill-Party-Planner Skill Package.
"""

from .skill import PartyPlannerSkill

def create_skill():
    return PartyPlannerSkill()

__all__ = ["PartyPlannerSkill", "create_skill"]
