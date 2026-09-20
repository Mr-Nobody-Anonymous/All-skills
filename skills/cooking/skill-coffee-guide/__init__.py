"""
Skill-Coffee-Guide Skill Package.
"""

from .skill import CoffeeGuideSkill

def create_skill():
    return CoffeeGuideSkill()

__all__ = ["CoffeeGuideSkill", "create_skill"]
