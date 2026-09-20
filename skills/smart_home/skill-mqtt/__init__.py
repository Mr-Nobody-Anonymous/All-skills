"""
Skill-Mqtt Skill Package.
"""

from .skill import MqttSkill

def create_skill():
    return MqttSkill()

__all__ = ["MqttSkill", "create_skill"]
