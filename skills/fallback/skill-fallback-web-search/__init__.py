"""
Skill-Fallback-Web-Search Skill Package.
"""

from .skill import FallbackWebSearchSkill

def create_skill():
    return FallbackWebSearchSkill()

__all__ = ["FallbackWebSearchSkill", "create_skill"]
