"""
Skill-Slideshow Skill Package.
"""

from .skill import SlideshowSkill

def create_skill():
    return SlideshowSkill()

__all__ = ["SlideshowSkill", "create_skill"]
