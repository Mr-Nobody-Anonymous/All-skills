"""
Skill-Obd-Diagnostics Skill Package.
"""

from .skill import ObdDiagnosticsSkill

def create_skill():
    return ObdDiagnosticsSkill()

__all__ = ["ObdDiagnosticsSkill", "create_skill"]
