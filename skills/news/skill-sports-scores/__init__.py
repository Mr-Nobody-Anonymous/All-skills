"""
Skill-Sports-Scores Skill Package.
"""

from .skill import SportsScoresSkill

def create_skill():
    return SportsScoresSkill()

__all__ = ["SportsScoresSkill", "create_skill"]
