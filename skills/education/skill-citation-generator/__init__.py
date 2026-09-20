"""
Skill-Citation-Generator Skill Package.
"""

from .skill import CitationGeneratorSkill

def create_skill():
    return CitationGeneratorSkill()

__all__ = ["CitationGeneratorSkill", "create_skill"]
