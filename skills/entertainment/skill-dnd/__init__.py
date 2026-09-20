"""
Skill-Dnd Skill Package.
"""

from .skill import DndSkill

def create_skill():
    return DndSkill()

__all__ = ["DndSkill", "create_skill"]
