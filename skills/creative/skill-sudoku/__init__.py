"""
Skill-Sudoku Skill Package.
"""

from .skill import SudokuSkill

def create_skill():
    return SudokuSkill()

__all__ = ["SudokuSkill", "create_skill"]
