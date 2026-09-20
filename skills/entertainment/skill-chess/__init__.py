"""
Skill-Chess Skill Package.
"""

from .skill import ChessSkill

def create_skill():
    return ChessSkill()

__all__ = ["ChessSkill", "create_skill"]
