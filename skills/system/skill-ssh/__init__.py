"""
Skill-Ssh Skill Package.
"""

from .skill import SshSkill

def create_skill():
    return SshSkill()

__all__ = ["SshSkill", "create_skill"]
