"""
Skill-Regex Skill Package.
"""

from .skill import RegexSkill

def create_skill():
    return RegexSkill()

__all__ = ["RegexSkill", "create_skill"]
