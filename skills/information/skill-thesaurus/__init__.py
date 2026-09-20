"""
Skill-Thesaurus Skill Package.
"""

from .skill import ThesaurusSkill

def create_skill():
    return ThesaurusSkill()

__all__ = ["ThesaurusSkill", "create_skill"]
