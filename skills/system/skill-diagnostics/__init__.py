"""
Skill-Diagnostics Skill Package.
"""

from .skill import DiagnosticsSkill

def create_skill():
    return DiagnosticsSkill()

__all__ = ["DiagnosticsSkill", "create_skill"]
