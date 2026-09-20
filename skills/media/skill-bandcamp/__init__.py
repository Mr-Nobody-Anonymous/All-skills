"""
Skill-Bandcamp Skill Package.
"""

from .skill import BandcampSkill

def create_skill():
    return BandcampSkill()

__all__ = ["BandcampSkill", "create_skill"]
