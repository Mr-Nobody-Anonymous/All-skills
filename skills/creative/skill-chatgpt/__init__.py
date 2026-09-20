"""
Skill-Chatgpt Skill Package.
"""

from .skill import ChatgptSkill

def create_skill():
    return ChatgptSkill()

__all__ = ["ChatgptSkill", "create_skill"]
