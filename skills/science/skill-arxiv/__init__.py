"""
Skill-Arxiv Skill Package.
"""

from .skill import ArxivSkill

def create_skill():
    return ArxivSkill()

__all__ = ["ArxivSkill", "create_skill"]
