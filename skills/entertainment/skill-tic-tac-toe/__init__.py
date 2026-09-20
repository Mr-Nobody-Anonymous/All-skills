"""
Skill-Tic-Tac-Toe Skill Package.
"""

from .skill import TicTacToeSkill

def create_skill():
    return TicTacToeSkill()

__all__ = ["TicTacToeSkill", "create_skill"]
