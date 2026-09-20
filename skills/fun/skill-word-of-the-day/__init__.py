"""
Skill-Word-Of-The-Day Skill Package.
"""

from .skill import WordOfTheDaySkill

def create_skill():
    return WordOfTheDaySkill()

__all__ = ["WordOfTheDaySkill", "create_skill"]
