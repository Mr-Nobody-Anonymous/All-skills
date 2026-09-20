"""
Skill-Typing-Tutor Skill Package.
"""

from .skill import TypingTutorSkill

def create_skill():
    return TypingTutorSkill()

__all__ = ["TypingTutorSkill", "create_skill"]
