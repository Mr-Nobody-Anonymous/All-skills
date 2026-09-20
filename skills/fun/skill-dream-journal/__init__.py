"""
Skill-Dream-Journal Skill Package.
"""

from .skill import DreamJournalSkill

def create_skill():
    return DreamJournalSkill()

__all__ = ["DreamJournalSkill", "create_skill"]
