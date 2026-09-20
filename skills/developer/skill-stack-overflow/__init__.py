"""
Skill-Stack-Overflow Skill Package.
"""

from .skill import StackOverflowSkill

def create_skill():
    return StackOverflowSkill()

__all__ = ["StackOverflowSkill", "create_skill"]
