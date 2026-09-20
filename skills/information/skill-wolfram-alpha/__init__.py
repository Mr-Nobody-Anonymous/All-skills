"""
Skill-Wolfram-Alpha Skill Package.
"""

from .skill import WolframAlphaSkill

def create_skill():
    return WolframAlphaSkill()

__all__ = ["WolframAlphaSkill", "create_skill"]
