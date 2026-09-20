"""
Skill-Fallback-Chatgpt Skill Package.
"""

from .skill import FallbackChatgptSkill

def create_skill():
    return FallbackChatgptSkill()

__all__ = ["FallbackChatgptSkill", "create_skill"]
