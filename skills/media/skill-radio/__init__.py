"""
Skill-Radio Skill Package.
"""

from .skill import RadioSkill

def create_skill():
    return RadioSkill()

__all__ = ["RadioSkill", "create_skill"]
