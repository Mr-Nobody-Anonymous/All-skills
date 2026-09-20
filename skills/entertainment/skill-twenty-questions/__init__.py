"""
Skill-Twenty-Questions Skill Package.
"""

from .skill import TwentyQuestionsSkill

def create_skill():
    return TwentyQuestionsSkill()

__all__ = ["TwentyQuestionsSkill", "create_skill"]
