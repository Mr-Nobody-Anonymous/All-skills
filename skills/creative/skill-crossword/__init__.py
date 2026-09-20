"""
Skill-Crossword Skill Package.
"""

from .skill import CrosswordSkill

def create_skill():
    return CrosswordSkill()

__all__ = ["CrosswordSkill", "create_skill"]
