"""
Skill-Hacker-News Skill Package.
"""

from .skill import HackerNewsSkill

def create_skill():
    return HackerNewsSkill()

__all__ = ["HackerNewsSkill", "create_skill"]
