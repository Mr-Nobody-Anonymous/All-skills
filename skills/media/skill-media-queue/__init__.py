"""
Skill-Media-Queue Skill Package.
"""

from .skill import MediaQueueSkill

def create_skill():
    return MediaQueueSkill()

__all__ = ["MediaQueueSkill", "create_skill"]
