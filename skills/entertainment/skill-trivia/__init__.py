"""
Skill-Trivia Skill Package.
"""

from .skill import TriviaSkill

def create_skill():
    return TriviaSkill()

__all__ = ["TriviaSkill", "create_skill"]
