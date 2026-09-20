"""
Skill-Json-Tools Skill Package.
"""

from .skill import JsonToolsSkill

def create_skill():
    return JsonToolsSkill()

__all__ = ["JsonToolsSkill", "create_skill"]
