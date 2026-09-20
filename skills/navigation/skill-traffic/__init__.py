"""
Skill-Traffic Skill Package.
"""

from .skill import TrafficSkill

def create_skill():
    return TrafficSkill()

__all__ = ["TrafficSkill", "create_skill"]
