"""
Skill-Docker Skill Package.
"""

from .skill import DockerSkill

def create_skill():
    return DockerSkill()

__all__ = ["DockerSkill", "create_skill"]
