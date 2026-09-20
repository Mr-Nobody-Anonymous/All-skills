"""
Skill-Philips-Hue Skill Package.
"""

from .skill import PhilipsHueSkill

def create_skill():
    return PhilipsHueSkill()

__all__ = ["PhilipsHueSkill", "create_skill"]
