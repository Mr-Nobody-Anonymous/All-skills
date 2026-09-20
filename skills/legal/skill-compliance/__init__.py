"""
Skill-Compliance Skill Package.
"""

from .skill import ComplianceSkill

def create_skill():
    return ComplianceSkill()

__all__ = ["ComplianceSkill", "create_skill"]
