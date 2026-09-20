"""
Skill-Lawyer-Finder Skill Package.
"""

from .skill import LawyerFinderSkill

def create_skill():
    return LawyerFinderSkill()

__all__ = ["LawyerFinderSkill", "create_skill"]
