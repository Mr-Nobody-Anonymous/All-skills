"""
Skill-Pubmed Skill Package.
"""

from .skill import PubmedSkill

def create_skill():
    return PubmedSkill()

__all__ = ["PubmedSkill", "create_skill"]
