"""
Skill-Security-System Skill Package.
"""

from .skill import SecuritySystemSkill

def create_skill():
    return SecuritySystemSkill()

__all__ = ["SecuritySystemSkill", "create_skill"]
