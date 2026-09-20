"""
Skill-Energy-Monitor Skill Package.
"""

from .skill import EnergyMonitorSkill

def create_skill():
    return EnergyMonitorSkill()

__all__ = ["EnergyMonitorSkill", "create_skill"]
