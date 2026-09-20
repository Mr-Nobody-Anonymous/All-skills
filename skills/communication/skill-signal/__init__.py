"""
Skill-Signal Skill Package.
"""

from .skill import SignalSkill

def create_skill():
    return SignalSkill()

__all__ = ["SignalSkill", "create_skill"]
