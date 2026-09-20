"""
Skill-Jokes Skill Package.
"""

from .skill import JokesSkill

def create_skill():
    return JokesSkill()

__all__ = ["JokesSkill", "create_skill"]
