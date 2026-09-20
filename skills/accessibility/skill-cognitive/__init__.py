"""
Skill-Cognitive Skill Package.
"""

from .skill import CognitiveSkill

def create_skill():
    return CognitiveSkill()

__all__ = ["CognitiveSkill", "create_skill"]
