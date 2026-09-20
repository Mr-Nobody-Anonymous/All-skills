"""
Skill-Speech Skill Package.
"""

from .skill import SpeechSkill

def create_skill():
    return SpeechSkill()

__all__ = ["SpeechSkill", "create_skill"]
