"""
Skill-Magic-8-Ball Skill Package.
"""

from .skill import Magic8BallSkill

def create_skill():
    return Magic8BallSkill()

__all__ = ["Magic8BallSkill", "create_skill"]
