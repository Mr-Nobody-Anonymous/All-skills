"""
Skill-Wine-Pairing Skill Package.
"""

from .skill import WinePairingSkill

def create_skill():
    return WinePairingSkill()

__all__ = ["WinePairingSkill", "create_skill"]
