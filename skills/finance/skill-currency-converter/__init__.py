"""
Skill-Currency-Converter Skill Package.
"""

from .skill import CurrencyConverterSkill

def create_skill():
    return CurrencyConverterSkill()

__all__ = ["CurrencyConverterSkill", "create_skill"]
