"""
Skill-Photo-Viewer Skill Package.
"""

from .skill import PhotoViewerSkill

def create_skill():
    return PhotoViewerSkill()

__all__ = ["PhotoViewerSkill", "create_skill"]
