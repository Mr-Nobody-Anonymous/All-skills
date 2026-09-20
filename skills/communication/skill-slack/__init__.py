"""
Skill-Slack Skill Package.
"""

from .skill import SlackSkill

def create_skill():
    return SlackSkill()

__all__ = ["SlackSkill", "create_skill"]
