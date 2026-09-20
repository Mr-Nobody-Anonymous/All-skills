"""
Skill-Code-Runner Skill Package.
"""

from .skill import CodeRunnerSkill

def create_skill():
    return CodeRunnerSkill()

__all__ = ["CodeRunnerSkill", "create_skill"]
