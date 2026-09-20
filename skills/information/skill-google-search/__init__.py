"""
Skill-Google-Search Skill Package.
"""

from .skill import GoogleSearchSkill

def create_skill():
    return GoogleSearchSkill()

__all__ = ["GoogleSearchSkill", "create_skill"]
