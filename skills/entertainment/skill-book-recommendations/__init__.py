"""
Skill-Book-Recommendations Skill Package.
"""

from .skill import BookRecommendationsSkill

def create_skill():
    return BookRecommendationsSkill()

__all__ = ["BookRecommendationsSkill", "create_skill"]
