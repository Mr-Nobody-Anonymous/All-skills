"""
Skill-Number-Converter Skill Package.
"""

from .skill import NumberConverterSkill

def create_skill():
    return NumberConverterSkill()

__all__ = ["NumberConverterSkill", "create_skill"]
