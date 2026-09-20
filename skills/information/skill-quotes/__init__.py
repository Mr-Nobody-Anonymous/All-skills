"""
Skill-Quotes Skill Package.
"""

from .skill import QuotesSkill

def create_skill():
    return QuotesSkill()

__all__ = ["QuotesSkill", "create_skill"]
