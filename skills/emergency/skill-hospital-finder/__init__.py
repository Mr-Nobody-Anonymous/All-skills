"""
Skill-Hospital-Finder Skill Package.
"""

from .skill import HospitalFinderSkill

def create_skill():
    return HospitalFinderSkill()

__all__ = ["HospitalFinderSkill", "create_skill"]
