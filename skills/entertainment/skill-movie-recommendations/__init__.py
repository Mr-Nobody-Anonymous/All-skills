"""
Skill-Movie-Recommendations Skill Package.
"""

from .skill import MovieRecommendationsSkill

def create_skill():
    return MovieRecommendationsSkill()

__all__ = ["MovieRecommendationsSkill", "create_skill"]
