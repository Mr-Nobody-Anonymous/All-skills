"""
Skill-Fallback-Wolfram Skill Package.
"""

from .skill import FallbackWolframSkill

def create_skill():
    return FallbackWolframSkill()

__all__ = ["FallbackWolframSkill", "create_skill"]
