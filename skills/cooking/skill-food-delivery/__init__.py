"""
Skill-Food-Delivery Skill Package.
"""

from .skill import FoodDeliverySkill

def create_skill():
    return FoodDeliverySkill()

__all__ = ["FoodDeliverySkill", "create_skill"]
