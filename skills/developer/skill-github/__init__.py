"""
Skill-Github Skill Package.
"""

from .skill import GithubSkill

def create_skill():
    return GithubSkill()

__all__ = ["GithubSkill", "create_skill"]
