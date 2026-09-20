"""
Skill-Breathing Skill Package.
"""

from .skill import BreathingSkill

def create_skill():
    return BreathingSkill()

__all__ = ["BreathingSkill", "create_skill"]
