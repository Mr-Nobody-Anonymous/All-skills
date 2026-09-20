"""
Skill-Thermostat Skill Package.
"""

from .skill import ThermostatSkill

def create_skill():
    return ThermostatSkill()

__all__ = ["ThermostatSkill", "create_skill"]
