"""
Skill-Coin-Flip Skill Package.
"""

from .skill import CoinFlipSkill

def create_skill():
    return CoinFlipSkill()

__all__ = ["CoinFlipSkill", "create_skill"]
