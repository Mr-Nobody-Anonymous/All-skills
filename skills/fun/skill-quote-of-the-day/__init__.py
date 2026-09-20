"""
Skill-Quote-Of-The-Day Skill Package.
"""

from .skill import QuoteOfTheDaySkill

def create_skill():
    return QuoteOfTheDaySkill()

__all__ = ["QuoteOfTheDaySkill", "create_skill"]
