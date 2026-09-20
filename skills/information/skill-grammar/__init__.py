"""
Skill-Grammar Skill Package.
"""

from .skill import GrammarSkill

def create_skill():
    return GrammarSkill()

__all__ = ["GrammarSkill", "create_skill"]
