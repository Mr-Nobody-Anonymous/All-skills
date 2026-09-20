"""
Skill-Tongue-Twisters Skill Package.
"""

from .skill import TongueTwistersSkill

def create_skill():
    return TongueTwistersSkill()

__all__ = ["TongueTwistersSkill", "create_skill"]
