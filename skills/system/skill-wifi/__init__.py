"""
Skill-Wifi Skill Package.
"""

from .skill import WifiSkill

def create_skill():
    return WifiSkill()

__all__ = ["WifiSkill", "create_skill"]
