"""
Skill-Market-News Skill Package.
"""

from .skill import MarketNewsSkill

def create_skill():
    return MarketNewsSkill()

__all__ = ["MarketNewsSkill", "create_skill"]
