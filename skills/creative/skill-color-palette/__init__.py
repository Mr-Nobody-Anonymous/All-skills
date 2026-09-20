"""
Skill-Color-Palette Skill Package.
"""

from .skill import ColorPaletteSkill

def create_skill():
    return ColorPaletteSkill()

__all__ = ["ColorPaletteSkill", "create_skill"]
