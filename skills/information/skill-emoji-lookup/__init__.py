"""
Skill-Emoji-Lookup Skill Package.
"""

from .skill import EmojiLookupSkill

def create_skill():
    return EmojiLookupSkill()

__all__ = ["EmojiLookupSkill", "create_skill"]
