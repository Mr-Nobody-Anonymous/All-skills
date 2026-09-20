"""
Skill-Server-Status Skill Package.
"""

from .skill import ServerStatusSkill

def create_skill():
    return ServerStatusSkill()

__all__ = ["ServerStatusSkill", "create_skill"]
