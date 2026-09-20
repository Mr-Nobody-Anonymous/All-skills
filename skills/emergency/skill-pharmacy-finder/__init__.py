"""
Skill-Pharmacy-Finder Skill Package.
"""

from .skill import PharmacyFinderSkill

def create_skill():
    return PharmacyFinderSkill()

__all__ = ["PharmacyFinderSkill", "create_skill"]
