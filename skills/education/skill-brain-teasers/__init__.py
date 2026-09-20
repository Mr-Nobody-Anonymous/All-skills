"""
Skill-Brain-Teasers Skill Package.
"""

from .skill import BrainTeasersSkill

def create_skill():
    return BrainTeasersSkill()

__all__ = ["BrainTeasersSkill", "create_skill"]
