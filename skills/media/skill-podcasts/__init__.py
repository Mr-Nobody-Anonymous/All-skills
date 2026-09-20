"""
Skill-Podcasts Skill Package.
"""

from .skill import PodcastsSkill

def create_skill():
    return PodcastsSkill()

__all__ = ["PodcastsSkill", "create_skill"]
