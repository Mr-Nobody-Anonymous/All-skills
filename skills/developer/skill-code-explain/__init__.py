"""
Skill-Code-Explain Skill Package.
"""

from .skill import CodeExplainSkill

def create_skill():
    return CodeExplainSkill()

__all__ = ["CodeExplainSkill", "create_skill"]
