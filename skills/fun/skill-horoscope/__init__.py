"""
Skill-Horoscope Skill Package.
"""

from .skill import HoroscopeSkill

def create_skill():
    return HoroscopeSkill()

__all__ = ["HoroscopeSkill", "create_skill"]
