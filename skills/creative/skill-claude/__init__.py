"""
Skill-Claude Skill Package.
"""

from .skill import ClaudeSkill

def create_skill():
    return ClaudeSkill()

__all__ = ["ClaudeSkill", "create_skill"]
