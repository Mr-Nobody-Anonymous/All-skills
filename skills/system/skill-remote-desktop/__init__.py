"""
Skill-Remote-Desktop Skill Package.
"""

from .skill import RemoteDesktopSkill

def create_skill():
    return RemoteDesktopSkill()

__all__ = ["RemoteDesktopSkill", "create_skill"]
