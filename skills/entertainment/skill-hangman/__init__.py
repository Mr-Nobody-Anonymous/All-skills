"""
Skill-Hangman Skill Package.
"""

from .skill import HangmanSkill

def create_skill():
    return HangmanSkill()

__all__ = ["HangmanSkill", "create_skill"]
