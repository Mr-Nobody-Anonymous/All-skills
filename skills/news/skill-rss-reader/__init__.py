"""
Skill-Rss-Reader Skill Package.
"""

from .skill import RssReaderSkill

def create_skill():
    return RssReaderSkill()

__all__ = ["RssReaderSkill", "create_skill"]
