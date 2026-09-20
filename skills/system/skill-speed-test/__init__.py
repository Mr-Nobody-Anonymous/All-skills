"""
Skill-Speed-Test Skill Package.
"""

from .skill import SpeedTestSkill

def create_skill():
    return SpeedTestSkill()

__all__ = ["SpeedTestSkill", "create_skill"]
