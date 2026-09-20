"""
Skill-Rhyme Skill Package.
"""

from .skill import RhymeSkill

def create_skill():
    return RhymeSkill()

__all__ = ["RhymeSkill", "create_skill"]
