"""
Skill-Flashcards Skill Package.
"""

from .skill import FlashcardsSkill

def create_skill():
    return FlashcardsSkill()

__all__ = ["FlashcardsSkill", "create_skill"]
