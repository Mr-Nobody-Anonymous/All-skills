"""
Skill-Storage Skill Package.
"""

from .skill import StorageSkill

def create_skill():
    return StorageSkill()

__all__ = ["StorageSkill", "create_skill"]
