"""
Skill-Movie-Info Skill Package.
"""

from .skill import MovieInfoSkill

def create_skill():
    return MovieInfoSkill()

__all__ = ["MovieInfoSkill", "create_skill"]
