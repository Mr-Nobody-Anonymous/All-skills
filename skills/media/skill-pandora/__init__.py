"""
Skill-Pandora Skill Package.
"""

from .skill import PandoraSkill

def create_skill():
    return PandoraSkill()

__all__ = ["PandoraSkill", "create_skill"]
