"""
Skill-Product-Info Skill Package.
"""

from .skill import ProductInfoSkill

def create_skill():
    return ProductInfoSkill()

__all__ = ["ProductInfoSkill", "create_skill"]
