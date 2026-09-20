"""
Skill-Process-Manager Skill Package.
"""

from .skill import ProcessManagerSkill

def create_skill():
    return ProcessManagerSkill()

__all__ = ["ProcessManagerSkill", "create_skill"]
