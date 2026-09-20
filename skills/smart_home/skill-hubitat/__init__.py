"""
Skill-Hubitat Skill Package.
"""

from .skill import HubitatSkill

def create_skill():
    return HubitatSkill()

__all__ = ["HubitatSkill", "create_skill"]
