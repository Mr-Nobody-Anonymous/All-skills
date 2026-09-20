"""
Skill-Dyslexia Skill Package.
"""

from .skill import DyslexiaSkill

def create_skill():
    return DyslexiaSkill()

__all__ = ["DyslexiaSkill", "create_skill"]
