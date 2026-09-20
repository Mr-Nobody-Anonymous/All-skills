"""
Skill-Wishlist Skill Package.
"""

from .skill import WishlistSkill

def create_skill():
    return WishlistSkill()

__all__ = ["WishlistSkill", "create_skill"]
