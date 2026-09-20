"""
Skill-Mastodon Skill Package.
"""

from .skill import MastodonSkill

def create_skill():
    return MastodonSkill()

__all__ = ["MastodonSkill", "create_skill"]
