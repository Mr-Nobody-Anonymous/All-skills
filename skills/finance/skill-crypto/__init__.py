"""
Skill-Crypto Skill Package.
"""

from .skill import CryptoSkill

def create_skill():
    return CryptoSkill()

__all__ = ["CryptoSkill", "create_skill"]
