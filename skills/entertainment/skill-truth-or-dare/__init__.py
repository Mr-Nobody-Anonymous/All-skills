"""
Skill-Truth-Or-Dare Skill Package.
"""

from .skill import TruthOrDareSkill

def create_skill():
    return TruthOrDareSkill()

__all__ = ["TruthOrDareSkill", "create_skill"]
