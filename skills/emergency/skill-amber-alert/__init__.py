"""
Skill-Amber-Alert Skill Package.
"""

from .skill import AmberAlertSkill

def create_skill():
    return AmberAlertSkill()

__all__ = ["AmberAlertSkill", "create_skill"]
