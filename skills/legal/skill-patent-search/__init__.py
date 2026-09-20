"""
Skill-Patent-Search Skill Package.
"""

from .skill import PatentSearchSkill

def create_skill():
    return PatentSearchSkill()

__all__ = ["PatentSearchSkill", "create_skill"]
