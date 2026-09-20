"""
Skill-Language-Learning Skill Package.
"""

from .skill import LanguageLearningSkill

def create_skill():
    return LanguageLearningSkill()

__all__ = ["LanguageLearningSkill", "create_skill"]
