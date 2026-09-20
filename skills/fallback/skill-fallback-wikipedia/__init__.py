"""
Skill-Fallback-Wikipedia Skill Package.
"""

from .skill import FallbackWikipediaSkill

def create_skill():
    return FallbackWikipediaSkill()

__all__ = ["FallbackWikipediaSkill", "create_skill"]
